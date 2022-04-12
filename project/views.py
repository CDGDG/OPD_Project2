from functools import reduce
import urllib
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator

from admin.models import Language
from developer.models import Developer
from recruit.models import Recruit, Recruit_Language
from company.models import Company

from .models import Document, Project, ProjectComment
from .forms import ProjectUpdateForm, Projectform

#파일 다운로드
import os
import mimetypes
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse


def list(request):
    all_projects = Project.objects.filter(private = False).order_by('-id')

    search = request.GET.get('s','')
    menu = request.GET.get('m', 'all')

    searchprojects = []

    flag = False

    for project in all_projects:

        if menu == 'title':
            print(project)
            if search in project.title:
                searchprojects.append(project)
        elif menu == 'member':
            if search in project.leader.nickname:
                searchprojects.append(project)
            else:
                for member in project.member.all():
                    if search in member.nickname:
                        searchprojects.append(project)
                        break
        elif menu == 'summary':
            if search in project.summary:
                searchprojects.append(project)
        elif menu == 'contents':
            if search in project.contents:
                searchprojects.append(project)
        elif menu == 'language':
            for lang in project.language.all():
                if search in lang.language:
                    searchprojects.append(project)
                    break

        elif menu == 'all':
            if search in project.title:
                searchprojects.append(project)
            elif search in project.summary:
                searchprojects.append(project)
            elif search in project.contents:
                searchprojects.append(project)
            elif search in project.leader.nickname:
                searchprojects.append(project)
            else:
                for member in project.member.all():
                    if search in member.nickname:
                        # searchprojects.append(project)
                        flag = True
                        break
                for lang in project.language.all():
                    if search in lang.language:
                        # searchprojects.append(project)
                        flag = True
                        break
                if flag:
                    searchprojects.append(project)
        else :
            searchprojects.append(project)

    # 페이징
    page = int(request.GET.get('p', 1))
    paginator = Paginator(searchprojects, 4) # 한 페이지당 5개씩 보여주는 Paginator 생성
    projects = paginator.get_page(page)

    return render(request, 'project_list.html', {'projects': projects, 'search': search, 'menu': menu})

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
    if not request.session.get('id'):
       return render(request,'no_login.html',{'next':"Project:list"})
    form = Projectform()
    return render(request, 'project_create.html', {'form': form})

def detail(request, pk):
    if not request.session.get('id'):
       return render(request,'no_login.html',{'next':"Project:list"})
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        raise Http404('프로젝트를 찾을 수 없습니다.')
    # 프로젝트 좋아요 여부
    docs = Document.objects.filter(project=project)
    id = request.session.get('id')
    is_like = None
    if id:
        try:
            if request.session.get('who')=="developer":
                is_like = Developer.objects.filter(id=id, likeproject=project).count()==1
            elif request.session.get('who')=='company':
                is_like = Company.objects.filter(id=id, likeproject=project).count()==1
        except Developer.DoesNotExist or Company.DoesNotExist:
            raise Http404('알 수 없는 사용자입니다.')
    # 댓글
    comments = ProjectComment.objects.filter(project=project)

    return render(request, 'project_detail.html', {'project': project, 'is_like': is_like, 'docs': docs, 'comments': comments})

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
        if not request.session.get('id'):
            return render(request,'no_login.html',{'next':"Project:list"})
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

def doc_download(request, pk):
    doc_file = get_object_or_404(Document, pk=pk)

    # doc_original = doc_file.docfile_original
    doc_original = urllib.parse.quote(doc_file.docfile_original.encode('utf-8'))

    root_path = os.path.join(settings.MEDIA_ROOT)# MEDIA root 경로
    file_name = doc_file.docfile.name # 물리적으로 저장되어 있는 파일명
    full_path = os.path.join(root_path,file_name)
    mimetype = mimetypes.guess_type(full_path)

    # 확인안되는 mimetype 의 경우. 기본적으로 'application/octet-stream' 으로 세팅
    if not mimetypes: mimetype = 'application/octet-stream'  
    file_size = os.path.getsize(full_path)

    fs = FileSystemStorage(root_path)
    response = FileResponse(fs.open(file_name, 'rb'), content_type=mimetype)

    response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'%s' % doc_original # 최초 업로드 당시 파일명 그대로 다운로드/ 한글 파일명 인코딩 후 다운로드
    response['Content-Length'] = file_size

    return response

def addcomment(request, pk):
    if request.method == "POST" and request.session.get('id'):
        project = get_object_or_404(Project,pk=pk)
        parentComment = request.POST.get('parentcomment', None)
        writer = get_object_or_404(Developer if request.session.get('who')=='developer' else Company, id=request.session.get('id'))
        contents = request.POST.get('contents','')
        pcomment = ProjectComment(
            project = project,
            contents = contents,
        )
        if parentComment:
            pcomment.parentComment = parentComment
        if request.session.get('who') == 'developer':
            pcomment.developer = writer
        elif request.session.get('who') == 'company':
            pcomment.company = writer
        pcomment.save()

        return JsonResponse({'data':'success'})

