from functools import reduce
import json
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from admin.models import Language
from recruit.forms import RecruitUpdateForm

from recruit.models import Recruit, Recruit_Language, RecruitOk
from developer.models import Developer
from project.models import Project
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
    apply = request.GET.get("apply", False)
    recruits = RecruitOk.objects.filter(project=recruit.project)
    return render(request, 'recruit_detail.html', {'recruit': recruit, 'apply': apply, 'recruits': recruits})

def update(request, pk):
    recruit = get_object_or_404(Recruit, pk=pk)
    if request.method=="POST":
        form = RecruitUpdateForm(request.POST, instance=recruit)
        if form.is_valid():
            recruit = form.save(commit=False)
            recruit.save()

            # 모집 언어
            if request.POST.get('num'):
                for i in range(int(request.POST.get('num'))):
                    if request.POST.get(f'select{i}'):
                        re_la = Recruit_Language(
                            recruit= recruit,
                            language= get_object_or_404(Language, id=request.POST.get(f"select{i}")),
                            people= request.POST.get(f"people{i}")
                        )
                        re_la.save()

            return redirect(f"/recruit/detail/{pk}/")
        else:
            print('recruit:update - form 검증 False')
    form = RecruitUpdateForm(instance=recruit)
    languages = reduce(lambda result, language: result.append(language) or result, Language.objects.all(), [])
    re_la = Recruit_Language.objects.filter(recruit = recruit)
    return render(request, 'recruit_update.html', {'form': form, 'pk': pk, 'languages': languages, 're_la': re_la})

def apply(request, pk):
    recruit = get_object_or_404(Recruit, pk=pk)
    if request.method=="POST":
        project = recruit.project
        developer = get_object_or_404(Developer, pk=request.session.get('id'))
        contents = request.POST.get('contents', '')
        recruitok = RecruitOk(
            project = project,
            developer = developer,
            contents = contents
        )
        recruitok.save()
    return redirect(f"/recruit/detail/{pk}/?apply=true")

def delete(request):
    if request.method=="POST":
        pk = request.POST.get('recruit_pk')
        if pk:
            recruit = get_object_or_404(RecruitOk, pk=pk)
            recruit.delete()
            return JsonResponse({'data':'success'})
    return redirect("/recruit/list/")

def accept(request):
    if request.method=="POST":
        pk = request.POST.get('recruit_pk')
        if pk:
            recruit = get_object_or_404(RecruitOk, pk=pk)
            recruit.project.member.add(recruit.developer)
            recruit.delete()
            return JsonResponse({'data':'success'})

def deleteRecruit_Language(request):
    if request.method=="POST":
        pk = request.POST.get('id')
        if pk:
            re_la = get_object_or_404(Recruit_Language, pk=pk)
            re_la.delete()
            return JsonResponse({'data': 'success'})