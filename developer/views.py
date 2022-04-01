from django.shortcuts import render
from .models import Developer
from .forms import JoinForm
from django.contrib.auth.hashers import make_password
# check_password

def join(request):
    if request.method=="POST":
        form = JoinForm(request.POST,request.FILES)
        if form.is_valid():
            developer = Developer()
            # developer = Developer(
            #         userid = form.userid,
            #         password = make_password(form.password),
            #         nickname = form.nickname,
            #         registnum = form.registnum,
            #         phonenum = form.phonenum,
            #         email = form.email,
            #         language = form.language,
            #         resume = request.FILES['resume'],
            #         # resume_original = form['resume'].name,
            #         pic = request.FILES['pic'],
            #         # pic_original = form['pic'].name,
            # )

            developer.userid = form.cleaned_data['userid']
            developer.save()

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