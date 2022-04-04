from django.http import JsonResponse
from django.shortcuts import redirect, render
from admin.models import Language
from .models import Developer
from .forms import JoinForm
from django.contrib.auth.hashers import make_password
# check_password

def home(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['developer'] = form.developer_pk
            return redirect("/")
    else:
        form = LoginForm()
        return render(request,"home.html",{'form':form})

def join(request):
    if request.method=="POST":
        form = JoinForm(request.POST,request.FILES)
        if form.is_valid():
            developer = Developer(
                    userid = form.userid,
                    password = make_password(form.password),
                    # password = form.password,
                    nickname = form.nickname,
                    registnum = form.registnum,
                    phonenum = form.phonenum,
                    email = form.email,
                    pic = request.FILES.get('pic'),
                    resume = request.FILES.get('resume'),
            )
            if developer.pic:
                developer.pic_original = developer.pic.name
            if developer.resume:
                developer.resume_original = developer.resume.name
            print(make_password(form.password))
        
            developer.save()
            
            for pk in form.language:
                if not pk: continue
                _language = Language.objects.get(pk=pk)
                developer.language.add(_language)

            return render(request,'home.html')
    else:
        form = JoinForm()
    return render(request,'developer_join.html',{'form':form})

def check_id(request):
    userid = request.GET.get('userid')
    context={}
    try:
        Developer.objects.get(userid=userid)
    except:
        context['data'] = "not exist"
    if userid=="":
        context['blank'] = True

    return JsonResponse(context)

def logout(request):
    if request.session.get('developer'):
        del(request.session['developer']) 
    return redirect('/') 




def info(request):
    if not request.session.get('developr'):
        return render(request,'home.html')
        
    return render(request,'developer_info.html')
def update(request):
    return render(request,'developer_update.html')
def myproject(request):
    return render(request,'developer_myproject.html')
def follow(request):
    return render(request,'developer_follow.html')