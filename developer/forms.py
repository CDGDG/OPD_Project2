from django import forms
from .models import Developer
from admin.models import Language
from django.contrib.auth.hashers import make_password

class JoinForm(forms.Form):
    userid = forms.CharField(
        error_messages={
            'required' : '아이디를 입력해주세요'
        },
        max_length=20,label='아이디'
    )
    password = forms.CharField(
        error_messages={
            'required' : '비밀번호를 입력해주세요'
        },
        widget=forms.PasswordInput,max_length=50,label='비밀번호'
    )
    check_passwored = forms.CharField(
        error_messages={
            'required' : '비밀번호를 입력해주세요'
        },
        widget=forms.PasswordInput,max_length=50,label='비밀번호 확인'
    )
    nickname = forms.CharField(
        error_messages={
            'required' : '닉네임를 입력해주세요'
        },
        max_length=15,label='닉네임'
    )
    registnum = forms.CharField(
        error_messages={
            'required' : '주민등록번호를 입력해주세요'
        },
        max_length=13,label='주민등록번호'
    )
    phonenum = forms.CharField(
        error_messages={
            'required' : '핸드폰번호를 입력해주세요'
        },
        max_length=11,label='핸드폰번호'
    )
    email = forms.EmailField(
        error_messages={
            'required' : '이메일을 입력해주세요'
        },
        max_length=15,label='이메일'
    )
    pic = forms.FileField(label='프로필사진')
    resume = forms.FileField(label='이력서')
    CHOICES = []
    for lang in Language.objects.all():
        CHOICES.append((lang.pk,lang.language))

    language = forms.MultipleChoiceField(label="언어 선택",widget=forms.CheckboxSelectMultiple, choices=CHOICES)

  
    def clean(self):
        cleaned_data = super().clean()
        self.userid = cleaned_data.get('userid')
        self.password = cleaned_data.get('password')
        self.check_password = cleaned_data.get('check_password')
        self.nickname = cleaned_data.get('nickname')
        self.registnum = cleaned_data.get('registnum')
        self.phonenum = cleaned_data.get('phonenum')
        self.email = cleaned_data.get('email')
        self.language = cleaned_data.get('language')

    
        # developer = Developer(
        #             userid = cleaned_data.get('userid'),
        #             password = cleaned_data.get('password'),
        #             nickname = cleaned_data.get('nickname'),
        #             registnum = cleaned_data.get('registnum'),
        #             phonenum = cleaned_data.get('phonenum'),
        #             email = cleaned_data.get('email'),
        #             language = cleaned_data.get('language'),
        #             resume = cleaned_data.get('resume'),
        #             pic = cleaned_data.get('pic'),
        # )
        # developer.save()
        
    










