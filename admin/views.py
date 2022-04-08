from django.shortcuts import render, redirect
from .forms import LoginForm, NoticeWriteForm
from django.urls import reverse_lazy
from company.forms import Company
from developer.forms import Developer
from django.contrib.auth.hashers import make_password, check_password
from django.http import Http404, JsonResponse
from .models import Admin, Notice
from django.core.paginator import Paginator
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView


def home(request):
    return render(request,"home.html")

def login(request):
    if request.method=="POST":
        form = LoginForm(request.POST)
        context={}
        if form.is_valid():
            select = request.POST.get('select', 'admin')
            print(select)
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
                            context['data'] = 'success login'
                            request.session['who'] = select
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
                            context['data'] = 'success login'
                            request.session['who'] = select
                            if company.pic:
                                request.session['pic_url'] = company.pic.url
                    elif select == 'admin':
                        admin = Admin.objects.get(adminid=userid)
                        if not check_password(password,admin.password):
                            # 비밀번호가 틀렸습니다.
                            context['data'] = "wrong password"
                        else:
                            request.session['id'] = admin.id
                            request.session['name'] = '관리자'
                            request.session['who'] = 'admin'
                            context['data'] = 'success login'
                            
                            
                except (Developer.DoesNotExist, Company.DoesNotExist, Admin.DoesNotExist):
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


def adminlogin(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'admin_login.html', {'form': form})
    # elif request.method=="POST":
    #     form = LoginForm(request.POST)
    #     context={}
    #     if form.is_valid():
    #         select = request.POST.get('select', 'developer')
    #         userid = form.userid
    #         password = form.password

    #         if userid and password:
    #             try:
    #                 admin = Admin.objects.get(adminid=userid)
    #                 if not check_password(password,admin.password):
    #                     # 비밀번호가 틀렸습니다.
    #                     context['data'] = "wrong password"
    #                 else:
    #                     request.session['id'] = admin.id
    #                     request.session['who'] = 'admin'
    #                     context['data'] = 'success login'
                            
    #             except (Admin.DoesNotExist):
    #                 # 아이디가 없습니다
    #                 context['data'] = "wrong id"
    #         else:
    #             context['blank'] = True
    #         return JsonResponse(context)

def noticelist(request):
    all_notices = Notice.objects.all().order_by('-id')


    search = request.GET.get('s','')
    menu = request.GET.get('m', 'all')

    searchnotices = []

    for notice in all_notices:

        if menu == 'title':
            if search in notice.title:
                searchnotices.append(notice)
        elif menu == 'contents':
            if search in notice.contents:
                searchnotices.append(notice)
        elif menu == 'all':
            if search in notice.title:
                searchnotices.append(notice)
            elif search in notice.contents:
                searchnotices.append(notice)
        else :
            searchnotices.append(notice)


    # 페이징
    page = int(request.GET.get('p', 1))
    paginator = Paginator(searchnotices, 10)  # 한 페이지당 10개씩 보여주는 paginator 생성
    notices = paginator.get_page(page)

    return render(request, 'notice_list.html', {'notices': notices, 'search': search, 'menu': menu})


def noticewrite(request):
    if request.method == "GET":
        form = NoticeWriteForm()
        return render(request, 'notice_write.html', {'form': form})
    if request.method == "POST":
        form = NoticeWriteForm(request.POST, request.FILES)
        if form.is_valid():
            notice = Notice(
                admin = Admin.objects.get(pk = request.session.get('id')),
                title = form.cleaned_data['title'],
                contents = form.cleaned_data['contents'],
                viewcnt = 0
            )
            notice.save()
        return render(request, 'notice_detail.html', {'notice': notice})


def noticedelete(request):
    if request.method == "POST":
        pk = request.POST.get('pk')
        notice = Notice.objects.get(pk = pk)
        notice.delete()  # DELETE


    return redirect('/admin/notice/list/')

def noticedetail(request, pk):
    try:
        notice = Notice.objects.get(pk = pk)
        notice.viewcnt += 1
        notice.save()
    except Notice.DoesNotExist:
        raise Http404('존재하지 않는 공지글입니다') # django에서 기본적으로 제공하는 에러 페이지
    return render(request, 'notice_detail.html', {'notice': notice})
    return redirect('/') 


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


class OPD_PasswordResetView(PasswordResetView):
    success_url = reverse_lazy('password_reset_done') # 성공시 호출 url
    template_name = "forgot_password/password_reset_form.html" # 자신의 password_reset.html 이동
    email_template_name = "forgot_password/password_reset_email.html"
    def form_valid(self, form):
        return super().form_valid(form)

class OPD_PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'forgot_password/password_reset_done.html'

