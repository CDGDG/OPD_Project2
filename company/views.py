from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from admin.models import Language
from .forms import CompanyJoinForm
from .models import Company
from django.core.paginator import Paginator

def list(request):
    all_companys = Company.objects.all().order_by('-id')

    # 페이징
    page = int(request.GET.get('p', 1))
    paginator = Paginator(all_companys, 5)  # 한 페이지당 5개씩 보여주는 paginator 생성
    companys = paginator.get_page(page)
    for company in companys:
        if company.category == 'big':
            company.category = '대기업'
        elif company.category == 'littlebig':
            company.category = '중견기업'
        elif company.category == 'small':
            company.category = '중소기업'
        elif company.category == 'start':
            company.category = '스타트업'

    return render(request, 'company_list.html', {'companys': companys})

def detail(request, pk):
    try:
        company = Company.objects.get(pk=pk)
        if company.category == 'big':
            company.category = '대기업'
        elif company.category == 'littlebig':
            company.category = '중견기업'
        elif company.category == 'small':
            company.category = '중소기업'
        elif company.category == 'start':
            company.category = '스타트업'

    except Company.DoesNotExist:
        raise Http404('존재하지 않는 기업입니다') # django에서 기본적으로 제공하는 에러 페이지
    return render(request, 'company_detail.html', {'company': company})

def update(request, pk):
    return render(request, 'update.html', {'pk':pk})

def delete(request, pk):
    return render(request, 'deleteOk.html', {'pk':pk})

def join(request):
    # GET 방식.  회원가입 폼
    if request.method == "GET":
        form = CompanyJoinForm()
        return render(request, 'company_join.html', {'form': form})
    # POST 방식.  회원가입 처리
    elif request.method == "POST":
        form = CompanyJoinForm(request.POST, request.FILES)
        if form.is_valid():
            company = Company(
                companyid = form.cleaned_data['companyid'],
                # password = form.cleaned_data['password'],
                password = make_password(form.cleaned_data['password']),
                name = form.cleaned_data['name'],
                tel = form.cleaned_data['tel'],
                email = form.cleaned_data['email'],
                address = form.cleaned_data['address'],
                address_detail = request.POST['address_detail'],
                people = form.cleaned_data['people'],
                url = form.cleaned_data['url'],
                summary = form.cleaned_data['summary'],
                category = form.cleaned_data['category'],
                pic = request.FILES['pic'],
                pic_original = request.FILES['pic'].name,
                # language = form.language
            )

            company.save()

            for pk in form.cleaned_data['language']:    # 선택한 언어 반복
                print("pk : ",pk)
                if not pk: continue
                _language = Language.objects.get(pk = pk) # 선택한 language의 pk로 language 정보 가져오기
                company.language.add(_language) # many to many 추가

            return redirect('/')

        return redirect('/company/join/')


def login(request):
    return render(request, 'login.html')

