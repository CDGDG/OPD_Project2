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
    all_recruits = Recruit.objects.filter(ing = True).order_by('-pk')

    search = request.GET.get('s','')
    menu = request.GET.get('m', 'all')

    searchrecruits = []

    for recruit in all_recruits:
        if menu == 'title':
            if search in recruit.title:
                searchrecruits.append(recruit)
        elif menu == 'contents':
            if search in recruit.contents:
                searchrecruits.append(recruit)
        elif menu == 'project':
            if search in recruit.project.title:
                searchrecruits.append(recruit)

        elif menu == 'all':
            if search in recruit.title:
                searchrecruits.append(recruit)
            elif search in recruit.contents:
                searchrecruits.append(recruit)
            elif search in recruit.project.title:
                searchrecruits.append(recruit)
        else :
            searchrecruits.append(recruit)

    # 페이징
    page = int(request.GET.get('p', 1))
    paginator = Paginator(searchrecruits, 4) # 한 페이지당 5개씩 보여주는 Paginator 생성
    recruits = paginator.get_page(page)

    return render(request, 'recruit_list.html', {"recruits": recruits, 'search': search, 'menu': menu})

def detail(request, pk):
    if not request.session.get('id'):
       return render(request,'no_login.html',{'next':"Recruit:list"})
    recruit = get_object_or_404(Recruit, pk=pk)
    apply = request.GET.get("apply", False)
    recruits = RecruitOk.objects.filter(project=recruit.project)
    re_la = Recruit_Language.objects.filter(recruit=recruit)
    me = None
    re_ok = None
    if request.session.get('who')=='developer':
        try:
            me = Developer.objects.get(pk=request.session.get('id',None))
            re_ok = recruits.filter(developer=me).count()>0
        except Developer.DoesNotExist:
            pass
    return render(request, 'recruit_detail.html', {'recruit': recruit, 'apply': apply, 'recruits': recruits, 're_la': re_la, 'me': me, 're_ok': re_ok})

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
            if not request.session.get('id'):
                return render(request,'no_login.html',{'next':"Recruit:list"})
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