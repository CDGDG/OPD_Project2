from functools import reduce
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator

from admin.models import Language
from developer.models import Developer
import project
from recruit.models import Recruit, Recruit_Language
from company.models import Company

from .models import Document, Project
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
                leader = get_object_or_404(Developer, id=request.session['id']),
                title = form.title,
                summary = form.summary,
                contents = form.contents,
                startdate = form.startdate,
                private = form.private,
                thumbnail = request.FILES.get('thumbnail'),  # 파일
            )
            if project.thumbnail:
                project.thumbnail_original = project.thumbnail.name  # 파일 원본 이름
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

    form = Projectform()
    return render(request, 'project_create.html', {'form': form})

def detail(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        raise Http404('프로젝트를 찾을 수 없습니다.')
    # 프로젝트 좋아요 여부
    id = request.session.get('id')
    if id:
        is_like = None
        try:
            if request.session.get('who')=="developer":
                is_like = Developer.objects.filter(id=id, likeproject=project).count()==1
            elif request.session.get('who')=='company':
                is_like = Company.objects.filter(id=id, likeproject=project).count()==1
        except Developer.DoesNotExist or Company.DoesNotExist:
            raise Http404('알 수 없는 사용자입니다.')
        print(is_like)

    return render(request, 'project_detail.html', {'project': project, 'is_like': is_like})

def update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    documents = Document.objects.filter(project=project)
    if request.method=="POST":
        form = ProjectUpdateForm(request.POST,request.FILES, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            if request.FILES.get('thumbnail'):
                project.thumbnail = request.FILES.get('thumbnail')
                project.thumbnail_original = request.FILES['thumbnail'].name

            project.save()
            # 문서
            docnum = request.POST.get('docnum')
            for i in range(int(docnum)):
                if request.FILES.get(f"doc{i}"):
                    document = Document(
                        project = project,
                        category = request.POST.get(f'doctype{i}'),
                        docfile = request.FILES.get(f"doc{i}"),
                        docfile_original = request.FILES.get(f"doc{i}").name
                    )
                    document.save()


            return redirect(f"/project/detail/{pk}/")
        else:
            print('project:update - form 검증 False')
    thumbnail, project.thumbnail = project.thumbnail, None
    form = ProjectUpdateForm(instance=project)
    return render(request, 'project_update.html', {'form': form, 'thumbnail': thumbnail, 'docs': documents,'pk': pk})


def delete(request):
    pk = request.POST.get('pk')
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return render(request, 'project_delete_ok.html')

def deleteDocument(request):
    pk = request.POST.get('id')
    try:
        document = Document.objects.get(pk=pk)
    except Document.DoesNotExist:
        return JsonResponse({'data': 'nodata'})
    document.delete()
    return JsonResponse({'data': 'success'})

def likeproject(request, pk):
    project = get_object_or_404(Project, pk=pk)
    who =  request.session.get('who')
    id = request.session.get('id')
    person = None
    if who and id:
        person = get_object_or_404(Developer if who=="developer" else Company, id=id)
        person.likeproject.add(project)
        return JsonResponse({'data': 'success'})
    return JsonResponse({'data': 'fail'})

def unlikeproject(request, pk):
    project = get_object_or_404(Project, pk=pk)
    who =  request.session.get('who')
    id = request.session.get('id')
    person = None
    if who and id:
        person = get_object_or_404(Developer if who=="developer" else Company, id=id)
        person.likeproject.remove(project)
        return JsonResponse({'data': 'success'})
    return JsonResponse({'data': 'fail'})