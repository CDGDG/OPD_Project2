from django import forms
from admin.models import Language
from django.contrib.auth.hashers import check_password

from developer.models import Developer

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
        widget=forms.PasswordInput,max_length=500,label='비밀번호'
    )
    check_passwored = forms.CharField(
        error_messages={
            'required' : '비밀번호를 입력해주세요'
        },
        widget=forms.PasswordInput,max_length=500,label='비밀번호 확인'
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
    email_id = forms.CharField(
        error_messages={
            'required' : '이메일을 입력해주세요'
        },
        max_length=50, label='이메일'
    )

    email_option = forms.CharField(
            error_messages={
                'required':'이메일을 입력해주세요'
            }, 
        max_length=50
        )
    pic = forms.ImageField(label='프로필사진', required=False)
    resume = forms.FileField(label='이력서', required=False)
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
        self.email_id = cleaned_data.get('email_id')
        self.email_option = cleaned_data.get('email_option')
        self.language = cleaned_data.get('language')

        

class LoginForm(forms.Form):
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
        widget=forms.PasswordInput,max_length=100,label='비밀번호'
    )


    def clean(self):
        cleaned_data = super().clean()

        self.userid = cleaned_data.get('userid')
        self.password = cleaned_data.get('password')

        if self.userid and self.password:
            try:
                developer = Developer.objects.get(userid=self.userid)
            except Developer.DoesNotExist:
                self.add_error('userid','아이디가 없습니다')
                return
            if not check_password(self.password,developer.password):
                self.add_error('password','비밀번호가 틀렸습니다')

            else:
                self.developer_pk = developer.pk