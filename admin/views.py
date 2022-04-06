from django.shortcuts import render, redirect
from .forms import LoginForm
from company.forms import Company
from developer.forms import Developer
from django.contrib.auth.hashers import make_password, check_password
from django.http import Http404, JsonResponse

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