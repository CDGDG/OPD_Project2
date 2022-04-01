from django.http import Http404
from django.shortcuts import redirect, render
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
    if request.method == "POST":
        form = Boardform(request.POST)
        if form.is_valid():
            developer_id = request.session.get('developer')
            developer = Developer.objects.get(pk=developer_id)

            board = Board()
            board.title = form.cleaned_data['title']
            board.contents = form.cleaned_data['contents']
            board.developer = developer
            board.save()

            # tags = form.cleaned_data['tags'].split(",")
            # for tag in tags:

            #     if not tag: continue

            #     _tag, created = Tag.objects.get_or_create(name=tag)

            #     board.tags.add(_tag)

            return redirect('/board/list/')
    else:
        form = Boardform()

    return render(request, 'board_create.html', {'form': form})


def board_detail(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404('게시글을 찾을수 없습니다')

    return render(request, 'board_detail.html', {'board': board})
    
def board_update(request, pk):
    pass
