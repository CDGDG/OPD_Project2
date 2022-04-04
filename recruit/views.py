from django.shortcuts import get_object_or_404, redirect, render
from recruit.forms import RecruitUpdateForm

from recruit.models import Recruit
from django.core.paginator import Paginator

def list(request):
    all_recruits = Recruit.objects.all().order_by('-pk')

    # 페이징
    page = int(request.GET.get('p', 1))
    paginator = Paginator(all_recruits, 5) # 한 페이지당 5개씩 보여주는 Paginator 생성
    recruits = paginator.get_page(page)

    return render(request, 'recruit_list.html', {"recruits": recruits})

def detail(request, pk):
    recruit = get_object_or_404(Recruit, pk=pk)
    return render(request, 'recruit_detail.html', {'recruit': recruit})

def update(request, pk):
    recruit = get_object_or_404(Recruit, pk=pk)
    if request.method=="POST":
        form = RecruitUpdateForm(request.POST, instance=recruit)
        if form.is_valid():
            recruit = form.save(commit=False)
            recruit.save()
            return redirect(f"/recruit/detail/{pk}/")
        else:
            print('recruit:update - form 검증 False')
    form = RecruitUpdateForm(instance=recruit)
    return render(request, 'recruit_update.html', {'form': form, 'pk': pk})

