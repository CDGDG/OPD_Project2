from functools import reduce
from turtle import width
from django import forms
from admin.models import Language
from company.models import Company
from django.contrib.auth.hashers import make_password, check_password


class CompanyJoinForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ['companyid', 'password', 're_password', 'name', 'category', 'summary', 'pic', 'tel', 'email', 'address', 'people', 'url', 'language']
        

    # companyid = forms.CharField(
    #     error_messages={
    #         'required': '아이디를 입력해주세요.'
    #     },
    #     max_length=20, label='아이디', initial=''
    # )

    
    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        max_length=500, label='비밀번호', widget=forms.PasswordInput, initial=''
    )

    re_password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        max_length=500, label='비밀번호 확인', widget=forms.PasswordInput, initial=''
    )

    name = forms.CharField(
        error_messages={
            'required': '회사 이름을 입력해주세요.'
        },
        max_length=15, label='회사 이름', initial=''
    )

    pic = forms.FileField(label='회사 사진')

    # tel = forms.CharField(
    #     error_messages={
    #         'required': '전화번호를 입력해주세요.'
    #     },
    #     max_length=20, label='회사 전화번호', initial=''
    # )

    # email = forms.EmailField(
    #     error_messages={
    #         'required': '이메일을 입력해주세요.'
    #     },
    #     label='이메일', initial=''
    # )

    # address = forms.CharField(
    #     error_messages={
    #         'required': '주소를 입력해주세요.'
    #     },
    #     label='주소', initial=''
    # )

    # people = forms.IntegerField(
    #     label='직원 수', initial=''
    # )

    url = forms.URLField(
        label='회사 홈페이지 URL', initial=''
    )

    summary = forms.CharField(
        label='회사소개', widget=forms.Textarea, initial=''
    )

    category = forms.ChoiceField(
        choices=(('', '회사 규모'),('big','대기업'),('littlebig','중견기업'),('small','중소기업'),('start','스타트업')),
        label='회사 규모', initial=''
    )

    LANGUAGE_OPTIONS = reduce(lambda result, lang: result.append((lang.id, lang.language)) or result,Language.objects.all(), [])

    language = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=LANGUAGE_OPTIONS, label='사용 언어')

    def clean(self):
        # 우선 부모 Form의 clean() 수행  -->  값이 들어있지 않으면 error 처리
        cleaned_data = super().clean()

        companyid = cleaned_data.get('companyid')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')
        name = cleaned_data.get('name')
        tel = cleaned_data.get('tel')
        email = cleaned_data.get('email')
        address = cleaned_data.get('address')
        people = cleaned_data.get('people')
        url = cleaned_data.get('url')
        summary = cleaned_data.get('summary')
        category = cleaned_data.get('category')
        pic = cleaned_data.get('pic')

        if password != re_password:
            self.add_error('re_password', '비밀번호가 서로 다릅니다.')
        
        print(tel.split('-'))
        if tel.split('-')[0] == '' or tel.split('-')[1] == '' or tel.split('-')[2] == '':
            self.add_error('tel', '전화번호를 형식에 맞게 입력해주세요.')



class CompanyUpdateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'pic', 'tel', 'email', 'address', 'people', 'url', 'summary', 'category', 'language']
    
    address = forms.CharField(
        error_messages={
            'required': '주소를 입력해주세요.'
        },
        label='주소', initial=''
    )
    
    url = forms.URLField(
        label='회사 홈페이지 URL', initial=''
    )

    category = forms.ChoiceField(
        choices=(('', '회사 규모'),('big','대기업'),('littlebig','중견기업'),('small','중소기업'),('start','스타트업')),
        label='회사 규모', initial=''
    )

    LANGUAGE_OPTIONS = reduce(lambda result, lang: result.append((lang.id, lang.language)) or result,Language.objects.all(), [])
    language = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=LANGUAGE_OPTIONS, label='언어 선택')

    def clean(self):
        # 우선 부모 Form의 clean() 수행  -->  값이 들어있지 않으면 error 처리
        cleaned_data = super().clean()

        tel = cleaned_data.get('tel')

        print(tel.split('-'))
        if tel.split('-')[0] == '' or tel.split('-')[1] == '' or tel.split('-')[2] == '':
            self.add_error('tel', '전화번호를 형식에 맞게 입력해주세요.')
    
    def __init__(self, *args, **kwargs):
        super(CompanyUpdateForm, self).__init__(*args, **kwargs)
        language = self.instance.language
        self.initial['language'] = [lang.id for lang in language.all()]





# class CompanySearchForm(forms.ModelForm):
#     class Meta:
#         model = Company
#         fields = ['menu', 'search']
#         widgets = {
#             'menu': forms.TextInput(attrs={
#                 'class': "form-control",
#                 }),
#             'search': forms.TextInput(attrs={
#                 'class': "form-control",
#                 }),
#             }

#     menu = forms.ChoiceField(
#         choices=(('all','전체'),('name','이름'),('tel','전화번호'),('email','이메일'),('address','주소'),('summary','소개')),
#         widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 10%'})
#     )
#     search = forms.CharField(
#         widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 60%'})
#     )


