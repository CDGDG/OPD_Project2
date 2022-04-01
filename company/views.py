from django.shortcuts import render, redirect
from .forms import CompanyJoinForm

def list(request):
    return render(request, 'list.html')

def detail(request, pk):
    return render(request, 'detail.html', {'pk':pk})

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
    # elif request.method == "POST":
    #     username = request.POST['username'] # name='username' 값을 받아온다
    #     useremail = request.POST['useremail']
    #     password = request.POST['password']
    #     re_password = request.POST['re-password']

    #     res_data = {}  # 템플릿에 전달할 context 데이터 준비

    #     # 데이터 검증. 빈 문자, 혹은 값이 없으면 에러 처리하기
    #     if not(username and useremail and password and re_password):
    #         res_data['error'] = '모든 값을 입력해야 합니다.'
    #     # password와 re-password가 다르면 회원가입 진행할 수 없다
    #     elif password != re_password:
    #         res_data['error'] = '비밀번호가 다릅니다.'
    #     else:
    #         # 받아온 값으로 User 생성
    #         user = User(
    #             username = username,
    #             useremail = useremail,
    #             password = make_password(password)  # 암호화 하여 저장
    #             )

    #         # DB에 저장
    #         user.save()

    #     return redirect('/')

def login(request):
    return render(request, 'login.html')

