from csv import writer
from functools import reduce
import json
import mimetypes
from multiprocessing import context
import re
from django.conf import settings
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from admin.models import Language
from developer.models import Developer
from company.models import Company
from .models import Boardimg, Board, Comment
from django.core.paginator import Paginator
from .forms import BoardUpdateForm, Boardform, CommentForm
import urllib
import os
from django.core.files.storage import FileSystemStorage

def board_list(request):
    boards_all = Board.objects.all().order_by('-id')

    search = request.GET.get('s','')
    menu = request.GET.get('m', 'all')
    # 메뉴
    searchboards = []

    for board in boards_all:
        if menu == 'developer':
            if search in board.developer.nickname:
                searchboards.append(board)
        elif menu == 'title':
            if search in board.title:
                searchboards.append(board)
        elif menu == 'language':
            for lang in board.language.all():
                if search in lang.language:
                    searchboards.append(board)
                    break

        elif menu == 'all':
            if search in board.developer.nickname:
                searchboards.append(board)
            elif search in board.title:
                searchboards.append(board)
            else :
                for lang in board.language.all():
                    if search in lang.language:
                        searchboards.append(board)
                        break
        else :
            searchboards.append(board)

    page = int(request.GET.get('p', 1)) # 없으면 1로 지정
    paginator = Paginator(searchboards, 10)   # 한 페이지당 10개씩 보여준다
    boards = paginator.get_page(page)

    return render(request, 'board_list.html', {'boards': boards,'search': search, 'menu': menu})

def board_create(request):
    # if not request.session.get('admin'):
    #     return redirect('Admin/login/')

    if request.method == 'POST':
        form = Boardform(request.POST, request.FILES)
        if form.is_valid():
            # developer_id = request.session.get('developer')
            # developer = Developer.objects.get(pk=developer_id)
            writer = Developer.objects.get(pk=request.session['id'])
            board = Board(
                title = form.title,
                developer = writer,
                contents = form.contents,
            )
            board.save()

            for _language in form.language:
                if not _language: continue
                board.language.add(Language.objects.get(pk=_language))

            # for _language in form.cleaned_data['language']:
            #     if not _language: continue
            #     board.language.add(Language.objects.get(pk=_language))

            # for pk in form.cleaned_data['language']:
            #     if not pk: continue
            #     _language = Language.objects.get(pk=pk)
            #     board.language.add(_language)
            if request.FILES.get('img'):
                boardimg = Boardimg(
                    img = request.FILES['img'],
                    img_original = request.FILES['img'].name,
                    board = board
                )
                boardimg.save()
            

            # comment = Comment(
            #     developer = board.developer + '작성자',
            #     contents = board.contents + '댓글 내용입니다',
            #     board = board
            # )
            # comment.save()


            return redirect(f'/board/detail/{board.pk}/')
    if not request.session.get('id'):
            return render(request,'no_login.html',{'next':"Board:list"})
    form = Boardform()
    # developer = request.session.get('developer_id')
    # nickname = Developer.objects.get(pk=developer).nickname
    

    return render(request, 'board_create.html', {'form': form})




def board_detail(request, pk):
    try:
        # board = Board.objects.get(pk=pk)
        board = get_object_or_404(Board, pk=pk)
        board.viewcnt += 1
        board.save() 
        print(board.developer)
        try:
            boardimg = Boardimg.objects.get(board = pk)
        except Boardimg.DoesNotExist:
            boardimg = ''

        try:
            comments = Comment.objects.filter(board = pk).order_by('-id')
        except Comment.DoesNotExist:
            comments = ''

    except Board.DoesNotExist:
        raise Http404('게시글을 찾을수 없습니다')

    return render(request, 'board_detail.html', {'board': board, 'boardimg': boardimg, 'comments': comments})

def filedownload(request, pk):
    boardimg = Boardimg.objects.get(pk=pk)

    # original_name = noticeimg.img_original  # 최초 업로드 당시 원본 파일명
    original_name = urllib.parse.quote(boardimg.img_original.encode('utf-8'))

    root_path = os.path.join(settings.MEDIA_ROOT) # MEDIA root 경로
    file_name = boardimg.img.name  # 물리적으로 저장되어 있는 파일명
    full_path = os.path.join(root_path, file_name)
    mimetype = mimetypes.guess_type(full_path)[0]  # (maintype, subtype) tuple 형태 -> ('image/png', None)

    # 확인 안되는 mimetype의 경우. 기본적으로 'application/octet-stream' 으로 세팅
    if not mimetype: mimetype = 'application/octet-stream'
    file_size = os.path.getsize(full_path)

    fs = FileSystemStorage(root_path)
    response = FileResponse(fs.open(file_name, 'rb'), content_type=mimetype)

    response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'%s' % original_name # 최초 업로드 당시 파일명 그대로 다운로드
    response['Content-Length'] = file_size
    return response
    

def board_update(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method=="POST":
        form = BoardUpdateForm(request.POST,request.FILES, instance=board)
        if form.is_valid():
            board = form.save(commit=False)
            if request.FILES.get('img'):
                boardimg = Boardimg.objects.get(board = pk)
                boardimg.img = request.FILES.get('img')
                boardimg.img_original = request.FILES['img'].name
                boardimg.save()

            board.save()
            return redirect(f"/board/detail/{pk}/")
        else:
            print('board:update - form 검증 False')
    if not request.session.get('id'):
        return render(request,'no_login.html',{'next':"Board:list"})
    form = BoardUpdateForm(instance=board)
    imgs = Boardimg.objects.filter(board = board)
    print(Boardimg.objects.filter(board = board))
    return render(request, 'board_update.html', {'form' : form, 'pk': pk, 'imgs': imgs})



def board_delete(request):
    pk = request.POST.get('pk')
    board = get_object_or_404(Board, pk=pk)
    board.delete()
    return render(request, 'board_deleteOk.html')


def comment_write(request, pk): 
    if request.method == 'POST':
        private = request.POST.get('private')
        print(private)
        board = Board.objects.get(pk= pk) 
        user = Developer.objects.get(pk = request.session.get('id')) if request.session.get('who') == 'developer' else Company.objects.get(pk = request.session.get('id'))
        print(private)
        if request.session.get('who') == 'developer':
            comment = Comment(
                board = board,
                developer = user,
                contents = request.POST.get('contents')
            )
            if private == 'on':
                comment.private = True
            comment.save()
            nickname = comment.developer.nickname
        elif request.session.get('who') == 'company':
            comment = Comment(
                board = board,
                company = user,
                contents = request.POST.get('contents')
            )
            if private == 'on':
                comment.private = True
            comment.save()
            nickname = comment.company.name
        pic = None
        if user.pic:
            pic = user.pic.url
        return JsonResponse({'data':'success', 'pk': comment.pk, 'who': request.session.get('who'), 'regdate': comment.regdate, 'contents': comment.contents, 'nickname': nickname, 'pic': pic})

        # return redirect(f'/board/detail/{pk}/')



def comment_delete(request):
    context = {}
    comment = Comment.objects.get(pk=request.POST.get('pk'))
    comment.delete()
    return JsonResponse(context)
