from django import forms
from admin.models import Language
from django.contrib.auth.hashers import check_password
from developer.models import Developer
from developer.widgets import PicPreviewWidget, ResumePreviewWidget

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
    re_password = forms.CharField(
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
            'required' : '휴대폰번호를 입력해주세요'
        },
        max_length=20,label='휴대폰번호'
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


        print("=========================================",cleaned_data)

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
            

class UpdateForm(forms.ModelForm):
    CHOICES = []
    for lang in Language.objects.all():
        CHOICES.append((lang.pk,lang.language))

    language = forms.MultipleChoiceField(label="언어 선택",widget=forms.CheckboxSelectMultiple, choices=CHOICES)

    pic = forms.ImageField(widget=PicPreviewWidget, allow_empty_file= True, required=False)
    resume = forms.FileField(widget=ResumePreviewWidget, allow_empty_file= True,required=False)

    class Meta:
        model = Developer
        fields = ['language','pic','resume']

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        language = self.instance.language
        self.initial['language'] = [lang.id for lang in language.all()]