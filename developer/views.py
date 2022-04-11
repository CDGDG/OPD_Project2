from datetime import datetime
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from admin.models import Language
from admin.views import logout
import developer
from project.models import Project
from .models import Developer, Follow
from .forms import JoinForm,UpdateForm
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator


#파일 다운로드
import os
import mimetypes
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse

#이메일 인증
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
# from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_text
# from .tokens import account_activation_token

def join(request):
    # 회원가입 처리
    if request.method=="POST":
        form = JoinForm(request.POST,request.FILES)
        if form.is_valid():
            print("join하기")
            developer = Developer(
                    userid = form.userid,
                    password = make_password(form.password),
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

            developer.save()

            for pk in form.language: # 선택한 언어 반복
                if not pk: continue 
                _language = Language.objects.get(pk=pk)
                developer.language.add(_language) # many to many
        else: 
            print("join 실패")
        return redirect("/")
    else:
        form = JoinForm()
        return render(request,'developer_join.html',{'form':form})

# 이메일 인증
def send_email(request):
        user_email = request.GET.get('email')
        emailnum = request.GET.get('emailnum') # 이메일 인증번호
        context={}
        current_site = get_current_site(request) 

        # 사용자에게 전송될 이메일 내용
        message = render_to_string('developer_activate_email.html', { 
            'domain': current_site.domain,
            'emailnum':emailnum, # 이메일로 보내질 인증번호
            # 'developer': developer,
            # 'uid': urlsafe_base64_encode(force_bytes(developer.pk)).encode().decode(),
            # 'token': account_activation_token.make_token(developer),
        })
        mail_title = "Our Project Diary 이메일 인증" # 이메일 title
        mail_to = user_email # 사용자 email
        email = EmailMessage(mail_title, message, to=[mail_to])
        if user_email == "":
            context['blank'] = True  # 이메일을 다 입력하지 않았을 때
        else:
            try: 
                email.send()
            except:
                context['fail'] = True # 이메일 전송 실패 시 
        return JsonResponse(context)

def check_id(request):
    userid = request.GET.get('userid')
    context={}
    try:
        Developer.objects.get(userid=userid) 
    except:
        context['data'] = "not exist" # 아이디 중복 없음
    if userid=="":
        context['blank'] = True # 아이디를 다 입력하지 않았을 때

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


def checkPassword(request):
    developer = Developer.objects.get(pk = request.session.get('id'))
    password = request.POST.get('password')
    check = request.POST.get('check')
    context = {}
    # info에서 수정하기 버튼 클릭시 비밀번호 확인
    if check == "check":
        if password == "":
            context['blank'] = True
        elif not check_password(password,developer.password):
            context['data'] = 'fail'
    # 수정할때 비밀번호확인
    else:
        if password:
            if check_password(password,developer.password):
                context['data'] = 'fail'

    return JsonResponse(context)

def info(request,pk):
    try:
        developer = Developer.objects.get(pk = pk)
    except Developer.DoesNotExist:
         raise Http404('정보를 찾을 수 없습니다')

    registnum = developer.registnum
    # 주민번호로 생년월일 , 성별  
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

    if request.session.get('id') == pk:
        return render(request,'developer_info.html',{'developer':developer,'birth':birth,'gender':gender,'password':developer.password})
    else:
        if Follow.objects.filter(developer=request.session.get('id'),follower = pk):
            follow_check = True
        else:
            follow_check = False
        return render(request,'developer_info.html',{'developer':developer,'birth':birth,'gender':gender,'password':developer.password,'follow_check':follow_check})



def download(request,pk):
    file = Developer.objects.get(pk=pk)

    resume_original = file.resume_original

    root_path = os.path.join(settings.MEDIA_ROOT)# MEDIA root 경로
    file_name = file.resume.name # 물리적으로 저장되어 있는 파일명
    full_path = os.path.join(root_path,file_name)
    mimetype = mimetypes.guess_type(full_path)

    # 확인안되는 mimetype 의 경우. 기본적으로 'application/octet-stream' 으로 세팅
    if not mimetypes: mimetype = 'application/octet-stream'  
    file_size = os.path.getsize(full_path)

    fs = FileSystemStorage(root_path)
    response = FileResponse(fs.open(file_name, 'rb'), content_type=mimetype)

    response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'%s''%"{resume_original}"' # 최초 업로드 당시 파일명 그대로 다운로드/ 한글 파일명 인코딩 후 다운로드
    response['Content-Length'] = file_size  

    return response

def update(request):
    if not request.session.get('id'):
        return render(request,'home.html')
    developer = Developer.objects.get(pk = request.session.get('id'))
    if request.method == "POST":
        old_password = developer.password
        new_password = request.POST.get('password')
        form = UpdateForm(request.POST,request.FILES,instance=developer)
        if form.is_valid():
            developer = form.save(commit=False)
            if new_password: 
                developer.password = make_password(new_password)
            else:
                developer.password = old_password

                if request.POST.get('pic_default') == "true": 
                    developer.pic = None
                else: 
                    if request.FILES.get('pic'):
                        developer.pic = request.FILES.get('pic')
                        developer.pic_original = developer.pic.name
            if request.FILES.get('resume'): 
                developer.resume = request.FILES.get('resume')
                developer.resume_original = developer.resume.name
            developer.save()
        return redirect(f'/developer/info/{developer.pk}/')
    else:
        pic, developer.pic= developer.pic, None
        # resume, developer.resume= developer.resume, None
        form = UpdateForm(instance=developer)
        return render(request,'developer_update.html',{'form':form,'pic':pic})

def myproject(request,pk):
    if not request.session.get('id'):
        return render(request,'home.html')
    developer = Developer.objects.get(pk=pk)
    projects = Project.objects.filter(leader = developer)
    return render(request, 'developer_myproject.html',{'projects':projects,'developer':developer})

def myfollowers(request):
    developer = Developer.objects.get(pk=request.session.get('id'))
    follow = Follow.objects.filter(developer = developer)
    
    return render(request,'developer_follow.html',{'follow':follow})


def follow(request):
    context={}
    follower = request.POST.get('developer_id')
    developer_follower = Developer.objects.get(pk = follower)
    developer = Developer.objects.get(pk = request.session.get('id'))
    if request.POST.get('check_follow') == "팔로우":
        print(follower)
        print(developer)
        follow = Follow(
            developer = developer,
            follower = developer_follower
        )
        follow.save()
    else:
        follow = Follow.objects.filter(developer=developer,follower=follower)
        follow.delete()
    return JsonResponse(context)
    

def list(request):

    all_developer = Developer.objects.all().order_by('id')

    search = request.GET.get('s','')
    menu = request.GET.get('m', 'all')
    #메뉴
    searchdeveloper = []
    for developer in all_developer:
        if menu == 'nickname':
            if search in developer.nickname:
                searchdeveloper.append(developer)
        elif menu == 'email':
            if search in developer.email:
                searchdeveloper.append(developer)
        elif menu == "language":
            for lang in developer.language.all():
                print("==========================",lang)
                if search in lang.language:
                    print("------------------",search)
                    searchdeveloper.append(developer)
        elif menu == 'all':
            if search in developer.nickname:
                searchdeveloper.append(developer)
            elif search in developer.email:
                searchdeveloper.append(developer)
        else :
            searchdeveloper.append(developer)
    
    #페이징
    page = int(request.GET.get('p', 1))
    paginator = Paginator(searchdeveloper, 10)  # 한 페이지당 10개씩 보여주는 paginator 생성
    developer = paginator.get_page(page)

    return render(request,'developer_list.html',{'developer':developer,'search':search,'menu':menu})


def leave(request):
    if request.method == "POST":
        developer = Developer.objects.get(pk = request.session.get('id'))
        developer.delete()
        return logout(request)
    return redirect("/")