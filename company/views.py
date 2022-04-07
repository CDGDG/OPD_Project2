from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from admin.models import Language
from .forms import CompanyJoinForm, CompanyUpdateForm
from .models import Company, CompanyFollow
from django.core.paginator import Paginator

def list(request):
    all_companys = Company.objects.all().order_by('-id')

    print(all_companys)

    search = request.GET.get('s','')
    menu = request.GET.get('m', 'all')

    searchcompanys = []

    for company in all_companys:
        if company.category == 'big':
            company.category = '대기업'
        elif company.category == 'littlebig':
            company.category = '중견기업'
        elif company.category == 'small':
            company.category = '중소기업'
        elif company.category == 'start':
            company.category = '스타트업'

        if menu == 'name':
            print(company)
            if search in company.name:
                searchcompanys.append(company)
        elif menu == 'tel':
            if search in company.tel:
                searchcompanys.append(company)
        elif menu == 'email':
            if search in company.email:
                searchcompanys.append(company)
        elif menu == 'address':
            if search in company.address:
                searchcompanys.append(company)
        elif menu == 'summary':
            if search in company.summary:
                searchcompanys.append(company)
        elif menu == 'all':
            if search in company.name:
                searchcompanys.append(company)
            elif search in company.tel:
                searchcompanys.append(company)
            elif search in company.email:
                searchcompanys.append(company)
            elif search in company.address:
                searchcompanys.append(company)
            elif search in company.summary:
                searchcompanys.append(company)
        else :
            searchcompanys.append(company)
    
    print(searchcompanys)


    # 페이징
    page = int(request.GET.get('p', 1))
    paginator = Paginator(searchcompanys, 10)  # 한 페이지당 10개씩 보여주는 paginator 생성
    companys = paginator.get_page(page)

    print(companys)

    # form = CompanySearchForm()

    print('s : ',search)
    print('m : ',menu)
    if search :
        print('sssssssssssssssss')
    if menu:
        print('mmmmmmmmmmmmmmm')


    return render(request, 'company_list.html', {'companys': companys, 'search': search, 'menu': menu})

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
        
        print('language - ',company.language)
        print('language - ',company.language.all())
        for language in company.language.all():
            print(language.pk)
        who = request.session.get('who')
        id = request.session.get('id')

    except Company.DoesNotExist:
        raise Http404('존재하지 않는 기업입니다') # django에서 기본적으로 제공하는 에러 페이지
    return render(request, 'company_detail.html', {'company': company})

def update(request, pk):
    if request.method == "GET":
        company = Company.objects.get(pk=pk)
        company.address = company.address.replace(" "," ")
        tellist = company.tel.split('-')
        form = CompanyUpdateForm(instance=company)
        print(company.address)
        print(company.address_detail)
        return render(request, 'company_update.html', {'form':form, 'company': company, 'tel1': tellist[0], 'tel2': tellist[1], 'tel3': tellist[2]})
        
    elif request.method == "POST":
        company = Company.objects.get(pk=pk)

        form = CompanyUpdateForm(request.POST, request.FILES, instance=company)
        if form.is_valid():

            company.address_detail = request.POST['address_detail']
            company = form.save(commit=False)
            # 수정
            # company.name = form.cleaned_data['name']
            # company.tel = form.cleaned_data['tel']
            # company.email = form.cleaned_data['email']
            # company.address = form.cleaned_data['address']
            
            # company.people = form.cleaned_data['people']
            # company.url = form.cleaned_data['url']
            # company.summary = form.cleaned_data['summary']
            # company.category = form.cleaned_data['category']
            # company.pic = request.FILES['pic']
            # company.pic_original = request.FILES['pic'].name
            company.save()  # UPDATE

            for id in form.cleaned_data['language']:    # 선택한 언어 반복
                if not pk: continue
                _language = Language.objects.get(id = id) # 선택한 language의 pk로 language 정보 가져오기
                company.language.add(_language) # many to many 추가

            return redirect(f'/company/detail/{pk}/')

        
        tellist = [request.POST['tel1'], request.POST['tel2'], request.POST['tel3']]
        return render(request, 'company_update.html', {'form': form, 'company': company, 'tel1': tellist[0], 'tel2': tellist[1], 'tel3': tellist[2]})

def delete(request):
    if request.method == "POST":
        pk = request.POST.get('pk')
        company = Company.objects.get(pk = pk)
        company.delete()  # DELETE

        # 세션 삭제
    if request.session.get('id'):   
        del(request.session['who'])
        del(request.session['id']) 
        del(request.session['name'])
        if request.session.get('pic_url'):
            del(request.session['pic_url']) 

    return redirect('/')

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

        # if request.POST['tel'] :
        # tellist = form.cleaned_data['tel'].split('-') if form.cleaned_data['tel'] else ['', '', '']
        # else:
            # tellist = ['', '', '']
        tellist = [request.POST['tel1'], request.POST['tel2'], request.POST['tel3']]

        print(tellist)
        return render(request,'company_join.html', {'form': form, 'tel1': tellist[0], 'tel2': tellist[1], 'tel3': tellist[2]})





def check_id(request):
    companyid = request.GET.get('companyid')
    context={}
    try:
        Company.objects.get(companyid=companyid)
    except:
        context['data'] = "not exist"
    if companyid=="":
        context['blank'] = True

    return JsonResponse(context)


def follow(request):
    print(request.session.get('id'))
    print(request.session['id'])
    session_id = int(request.session.get('id'))
    print(session_id)

    all_follow = []
    # print(CompanyFollow.objects.get(company = session_id))
    for follow in CompanyFollow.objects.all().order_by('-id'):
        print(follow.follower.nickname)
        if follow.company.id == session_id:
            print('zzzzzzzzzzzzz')
            all_follow.append(follow.follower)
        
    search = request.GET.get('s','')
    menu = request.GET.get('m', 'all')

    searchfollows = []

    for follow in all_follow:

        if menu == 'nickname':
            print(follow)
            if search in follow.nickname:
                searchfollows.append(follow)
        elif menu == 'phonenum':
            if search in follow.phonenum:
                searchfollows.append(follow)
        elif menu == 'email':
            if search in follow.email:
                searchfollows.append(follow)
        elif menu == 'all':
            if search in follow.nickname:
                searchfollows.append(follow)
            elif search in follow.phonenum:
                searchfollows.append(follow)
            elif search in follow.email:
                searchfollows.append(follow)
        else :
            searchfollows.append(follow)



    page = int(request.GET.get('p', 1))
    paginator = Paginator(searchfollows, 1)  # 한 페이지당 10개씩 보여주는 paginator 생성
    follows = paginator.get_page(page)

    return render(request, 'company_follow.html', {'follows': follows, 'search': search, 'menu': menu})

