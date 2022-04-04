from django.shortcuts import redirect, render
from admin.models import Language
from .models import Developer
from .forms import JoinForm
from django.contrib.auth.hashers import make_password
# check_password



def join(request):
    if request.method=="POST":
        form = JoinForm(request.POST,request.FILES)
        if form.is_valid():
            developer = Developer(
                    userid = form.userid,
                    password = make_password(form.password),
                    nickname = form.nickname,
                    registnum = form.registnum,
                    phonenum = form.phonenum,
                    email = form.email,
                    pic = request.FILES['pic'],
                    pic_original = request.FILES['pic'].name,
                    resume = request.FILES['resume'],
                    resume_original = request.FILES['resume'].name,
            )
        
            developer.save()
            
            for pk in form.language:
                if not pk: continue
                _language = Language.objects.get(pk=pk)
                developer.language.add(_language)

            return render(request,'developer_join.html')
    else:
        form = JoinForm()
    return render(request,'developer_join.html',{'form':form})


def info(request):
    return render(request,'developer_info.html')
def update(request):
    return render(request,'developer_update.html')
def myproject(request):
    return render(request,'developer_myproject.html')
def follow(request):
    return render(request,'developer_follow.html')