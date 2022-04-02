from functools import reduce
from django.shortcuts import redirect, render
from django.core.paginator import Paginator

from admin.models import Language

from .models import Project
from .forms import Projectform

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

            for pk in form.language:    # 선택한 언어 반복
                if not pk: continue
                _language = Language.objects.get(pk = pk) # 선택한 language의 pk로 language 정보 가져오기
                project.language.add(_language) # many to many 추가


            return redirect('/project/list/')
        else:
            print(request.FILES)

    form = Projectform()
    return render(request, 'project_create.html', {'form': form})
