from datetime import datetime
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from admin.models import Language
from .models import Developer
from .forms import DeveloperUpdateForm, JoinForm,LoginForm
from django.contrib.auth.hashers import make_password, check_password

#이메일 인증
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
# from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_text
# from .tokens import account_activation_token

def login(request):
    if request.method=="POST":
        form = LoginForm(request.POST)
        context={}
        if form.is_valid():
            userid = form.userid
            password = form.password

            if userid and password:
                try:
                    developer = Developer.objects.get(userid=userid)
                    if not check_password(password,developer.password):
                        # 비밀번호가 틀렸습니다.
                        context['data'] = "wrong password"
                    else:
                        print(userid + "로그인 성공" + developer.nickname)
                        request.session['developer_id'] = developer.id
                        request.session['developer_nickname'] = developer.nickname
                        if developer.pic:
                            request.session['developer_pic_url'] = developer.pic.url
                        context['data'] = 'success login'
                except Developer.DoesNotExist:
                    # 아이디가 없습니다
                    context['data'] = "wrong id"
            else:
                context['blank'] = True
            return JsonResponse(context)
    else:
        return redirect("/")

    
    # if request.method == "POST":
    #     form = LoginForm(request.POST)
    #     if form.is_valid():
    #         print("로그인 성공")
    #         request.session['developer'] = form.developer_pk
    #         return redirect("/")
    # return render(request,"home.html")

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
                    email = form.email_id+"@"+form.email_option,
                    pic = request.FILES.get('pic'),
                    resume = request.FILES.get('resume'),
            )
            if developer.pic:
                developer.pic_original = developer.pic.name
            if developer.resume:
                developer.resume_original = developer.resume.name
            developer.save()
            for pk in form.language:
                if not pk: continue
                _language = Language.objects.get(pk=pk)
                developer.language.add(_language)

        return redirect("/")
    else:
        form = JoinForm()
    return render(request,'developer_join.html',{'form':form})

def send_email(request):
        email_id = request.GET.get('email_id')
        email_option = request.GET.get('email_option')
        emailnum = request.GET.get('emailnum')
        context={}
        current_site = get_current_site(request) 
        message = render_to_string('developer_activate_email.html', {
            'domain': current_site.domain,
            'emailnum':emailnum,
            # 'developer': developer,
            # 'uid': urlsafe_base64_encode(force_bytes(developer.pk)).encode().decode(),
            # 'token': account_activation_token.make_token(developer),
        })
        mail_title = "Our Project Diary 이메일 인증"
        mail_to = email_id+"@"+email_option
        email = EmailMessage(mail_title, message, to=[mail_to])
        try: 
            email.send()
        except:
            context['fail'] = True
        if email_id == "" or email_option =="":
            context['blank'] = True
        return JsonResponse(context)


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


def check_nick(request):
    nickname = request.GET.get('nickname')
    context={}
    try:
        Developer.objects.get(nickname=nickname)
    except:
        context['data'] = "not exist"
    if nickname=="":
        context['blank'] = True

    return JsonResponse(context)



def logout(request):
    if request.session.get('developer_id'):
        del(request.session['developer_id']) 
        del(request.session['developer_nickname'])
        if request.session.get('developer_pic_url'):
            del(request.session['developer_pic_url']) 
    return redirect('/') 


def info(request):
    # if not request.session.get('developr'):
    #     return render(request,'home.html')
    try:
        developer = Developer.objects.get(pk = request.session.get('developer_id'))
        registnum = developer.registnum
        
        birth = {}
        if int(registnum[:2]) < 21 and int(registnum[6]) in (3, 4) :
            birth['year']= 2000 + int(registnum[:2])
        else:
            birth['year'] = 1900 + int(registnum[:2])

        birth['age'] = datetime.today().year - birth['year'] + 1
        birth['month'] = registnum[2:4]
        birth['day'] = registnum[4:6]

        if int(registnum[6]) == 1 or int(registnum[6]) == 3 :
            gender = 'male'
        else :
            gender = 'female'
    except Developer.DoesNotExist:
         raise Http404('내 정보를 찾을 수 없습니다')
    
    return render(request,'developer_info.html',{'developer':developer,'birth':birth,'gender':gender})

def update(request):
      # if not request.session.get('developr'):
    #     return render(request,'home.html')
    developer = Developer.objects.get(pk = request.session.get('developer_id'))
    if request.method == "POST":
        form = DeveloperUpdateForm(request.POST,request.FILES,instance=developer)
        if form.is_valid():
            developer = form.save(commit=False)
            if developer.pic:
                developer.pic_original = developer.pic.name
            if developer.resume:
                developer.resume_original = developer.resume.name
            developer.save()
            return redirect("/developer/info/")
    else:
        form = DeveloperUpdateForm(instance=developer)
    return render(request,'developer_update.html',{'form':form})


def myproject(request):
    # myprojects = Developer.


    return render(request,'developer_myproject.html')
def follow(request):
    return render(request,'developer_follow.html')