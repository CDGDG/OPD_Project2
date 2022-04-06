from xml.etree.ElementTree import Comment
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from admin.models import Language
from .models import Boardimg
from .models import Board
from django.core.paginator import Paginator
from .forms import Boardform
from developer.models import Developer


def board_list(request):
    boards_all = Board.objects.all().order_by('-id')
    page = int(request.GET.get('p', 1)) # 없으면 1로 지정
    paginator = Paginator(boards_all, 10)   # 한 페이지당 10개씩 보여준다
    boards = paginator.get_page(page)

    return render(request, 'board_list.html', {'boards': boards})

def board_create(request):
    if request.method == 'POST':
        form = Boardform(request.POST, request.FILES)
        if form.is_valid():
            board = Board(
                title = form.title,
                developer = form.developer,
                contents = form.contents,
            )
            board.save()

            for _language in form.language:
                if not _language: continue
                board.language.add(Language.objects.get(pk=_language))

            boardimg = Boardimg(
                img = request.FILES['img'],
                img_original = request.FILES['img'].name,
                board = board
            )
            boardimg.save()


            comment = Comment(
                developer = board.developer + '작성자',
                contents = board.contents + '댓글 내용입니다',
                board = board
            )
            comment.save()


            return redirect(f'/board/detail/{board.pk}/')
        else:
            print(request.FILES)

    form = Boardform()
    developerid = request.session.get('developer_id')
    nickname = Developer.objects.get(pk=developerid).nickname

    return render(request, 'board_create.html', {'form': form, 'nickname': nickname})

def board_detail(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404('게시글을 찾을수 없습니다')

    return render(request, 'board_detail.html', {'board': board})
    
def board_update(request, pk):
    # board = get_object_or_404(Board, pk=pk)
    # if request.method=="POST":
    #     form = BoardUpdateForm(request.POST, instance=board)
    #     if form.is_valid():
    #         board = form.save(commit=False)
    #         board.save()
    #         return redirect(f"/board/detail/{pk}/")
    #     else:
    #         print('board:update - form 검증 False')
    #     form = BoardUpdateForm(instance=board)
    #     return render(request, 'board_update.html', {'form' : form, 'pk': pk})

    if request.method == "GET":
        try:
            board = Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            raise Http404('게시글을 찾을수 없습니다')

        return render(request, 'board/update.html', {'board': board})
    
    elif request.method == "POST":
        img = request.POST['img']
        img_original = request.POST['img_original']

        board = Board.objects.get(pk=pk)
        board.img = img
        board.img_original = img_original
        board.save()

        return render(request, 'board/updateOk.html', {"pk": board.pk})
        
def board_delete(request):
    pk = request.POST.get('pk')
    board = get_object_or_404(Board, pk=pk)
    board.delete()
    return render(request, 'board_deleteOk.html')
