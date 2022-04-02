from django.shortcuts import render
from admin.models import Language
from .models import Developer
from .forms import JoinForm
from django.contrib.auth.hashers import make_password
# check_password

def join(request):
    if request.method=="POST":
        form = JoinForm(request.POST,request.FILES)
        if form.is_valid():
            # developer = Developer()
            print("==========",request.FILES['resume'].name,"================")
            developer = Developer(
                    userid = form.userid,
                    password = form.password,
                    nickname = form.nickname,
                    registnum = form.registnum,
                    phonenum = form.phonenum,
                    email = form.email,
                    # resume = request.FILES.get('resume'),
                    resume = request.FILES['resume'],
                    resume_original = request.FILES['resume'].name,
                    # pic = request.FILES.get('pic'),
                    pic = request.FILES['pic'],
                    pic_original = request.FILES['pic'].name,
            )
        
            # developer.userid = form.cleaned_data['userid']
            # developer.password=form.cleaned_data['password']
            # developer.nickname =form.cleaned_data['nickname']
            # developer.registnum=form.cleaned_data['registnum']
            # developer.phonenum=form.cleaned_data['phonenum']
            # developer.resume = request.FILES['resume']
            # developer.email=form.cleaned_data['email']
            # developer.pic = request.FILES['pic']
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