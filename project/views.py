from functools import reduce
from turtle import title
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator

from admin.models import Language
from recruit.models import Recruit, Recruit_Language

from .models import Project
from .forms import ProjectUpdateForm, Projectform

def list(request):
    all_projects = Project.objects.all().order_by('-id')

    # 페이징
    page = int(request.GET.get('p', 1))
    paginator = Paginator(all_projects, 5) # 한 페이지당 5개씩 보여주는 Paginator 생성
    projects = paginator.get_page(page)

    return render(request, 'project_list.html', {"projects": projects})

def create(request):
    if request.method == "POST":
        form = Projectform(request.POST, request.FILES)
        if form.is_valid():
            project = Project(
                title = form.title,
                summary = form.summary,
                contents = form.contents,
                startdate = form.startdate,
                private = form.private,
                thumbnail = request.FILES['thumbnail'],  # 파일
                thumbnail_original = request.FILES['thumbnail'].name  # 파일 원본 이름
            )
            project.save()  # many to many 넣어주기 전에 project의 pk가 필요하므로 미리 save

            for _language in form.language:    # 선택한 언어 반복
                if not _language: continue
                project.language.add(Language.objects.get(pk=_language)) # many to many 추가

            recruit = Recruit(
                title = project.title + "모집",
                contents = project.title + '모집 내용입니다.',
                ing = False,
                project = project
            )
            recruit.save()

            for _language in form.language:
                recru_lang = Recruit_Language(
                    recruit = recruit,
                    language = Language.objects.get(pk=_language),
                    people = 0
                )
                recru_lang.save()

            return redirect(f'/project/detail/{project.pk}/')
        else:
            print(request.FILES)

    form = Projectform()
    return render(request, 'project_create.html', {'form': form})

def detail(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        raise Http404('프로젝트를 찾을 수 없습니다.')
    return render(request, 'project_detail.html', {'project': project})

def update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method=="POST":
        form = ProjectUpdateForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            return redirect(f"/project/detail/{pk}/")
        else:
            print('project:update - form 검증 False')
    form = ProjectUpdateForm(instance=project)
    return render(request, 'project_update.html', {'form': form, 'pk': pk})


def delete(request):
    pk = request.POST.get('pk')
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return render(request, 'project_delete_ok.html')