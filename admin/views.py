from django.shortcuts import render, redirect
from .forms import LoginForm
from company.forms import Company
from developer.forms import Developer
from django.contrib.auth.hashers import make_password, check_password
from django.http import Http404, JsonResponse

# 비밀번호 찾기_이메일 전송
from functools import reduce
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import string
import random


def home(request):
    return render(request,"home.html")

def login(request):
    if request.method=="POST":
        form = LoginForm(request.POST)
        context={}
        if form.is_valid():
            select = request.POST.get('select', 'developer')
            userid = form.userid
            password = form.password

            if select and userid and password:
                try:
                    if select=="developer":
                        developer = Developer.objects.get(userid=userid)
                        if not check_password(password,developer.password):
                            # 비밀번호가 틀렸습니다.
                            context['data'] = "wrong password"
                        else:
                            request.session['id'] = developer.id
                            request.session['name'] = developer.nickname
                            if developer.pic:
                                request.session['pic_url'] = developer.pic.url
                    elif select=="company":
                        company = Company.objects.get(companyid = userid)
                        if not check_password(password, company.password):
                            # 비밀번호가 틀렸습니다.
                            context['data'] = 'wrong password'
                        else:
                            request.session['id'] = company.id
                            request.session['name'] = company.name
                            if company.pic:
                                request.session['pic_url'] = company.pic.url
                            
                    context['data'] = 'success login'
                    request.session['who'] = select
                except (Developer.DoesNotExist, Company.DoesNotExist):
                    # 아이디가 없습니다
                    context['data'] = "wrong id"
            else:
                context['blank'] = True
            return JsonResponse(context)
    else:
        return redirect("/")

def logout(request):
    if request.session.get('id'):
        del(request.session['who'])
        del(request.session['id']) 
        del(request.session['name'])
        if request.session.get('pic_url'):
            del(request.session['pic_url']) 
    return redirect('/') 

# 이메일 전송을 위한 아이디 체크
def check_userid(request):
    if request.method=="POST":
        context={}
        select = request.POST.get('select', 'developer')
        userid = request.POST.get('userid')
        if select and userid:
            try:
                if select=="developer":
                    Developer.objects.get(userid=userid)
                elif select=="company":
                    Company.objects.get(companyid = userid)      
                context['data'] = 'success'
            except (Developer.DoesNotExist, Company.DoesNotExist):
                # 아이디가 없습니다
                context['data'] = "wrong id"
        else:
            context['blank'] = True
        return JsonResponse(context)     
    else:
        return render(request,'forgot_password.html')

# 이메일로 비밀번호 전송
def reset_password(request):
        who = request.POST.get('who')
        userid = request.POST.get('userid')

        # 비밀번호 생성
        resetpassword = string.ascii_letters+string.digits
        new_password = reduce(lambda p, x: p + random.choice(resetpassword), range(15), "")+"@"


        context={}
        if who == "developer":
            developer = Developer.objects.get(userid=userid)
            mail_to = developer.email # 사용자 email
            context['email'] = mail_to
            developer.password = make_password(new_password) # 생성된 비밀번호 update
            developer.save()
        else:
            company = Company.objects.get(companyid = userid)
            mail_to = company.email
            context['email'] = mail_to
            company.password = make_password(new_password)
            company.save()
    
        # 사용자에게 전송될 이메일 
        current_site = get_current_site(request)
        message = render_to_string('password_reset_email.html', { 
            'domain': current_site.domain,
            'new_password':new_password, # 이메일로 보내질 비밀번호
            # 'developer': developer,
            # 'uid': urlsafe_base64_encode(force_bytes(developer.pk)).encode().decode(),
            # 'token': account_activation_token.make_token(developer),
        })
        mail_title = "Our Project Diary 비밀번호 변경" # 이메일 title
        email = EmailMessage(mail_title, message, to=[mail_to])
        try: 
            email.send()
        except:
            context['fail'] = True # 이메일 전송 실패 시 

        return render(request,'password_reset_done.html',context)



# class OPD_PasswordResetView(PasswordResetView):
#     success_url = reverse_lazy('password_reset_done') # 성공시 호출 url
#     template_name = "forgot_password/password_reset_form.html" # 자신의 password_reset.html 이동
#     # email_template_name = "forgot_password/password_reset_email.html"
#     def form_valid(self, form):
#         return super().form_valid(form)

# class OPD_PasswordResetDoneView(PasswordResetDoneView):
#     template_name = 'forgot_password/password_reset_done.html'

    