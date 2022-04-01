from django.shortcuts import redirect, render
from django.core.paginator import Paginator

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
                thumbnail = request.FILES['thumbnail'],
                # language = form.language
            )

            project.save()

            return redirect('/project/list/')
        else:
            print(request.FILES)

    form = Projectform()
    return render(request, 'project_create.html', {'form': form})
