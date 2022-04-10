from functools import reduce
from django import forms
from .models import Notice, Language


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


class NoticeWriteForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'contents', 'file']
        labels = {
            "title": "제목",
            "contents": "내용"
        }
    
    file = forms.FileField(allow_empty_file= True, label='첨부파일', required=False)


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['language']

    LANGUAGE_OPTIONS = reduce(lambda result, lang: result.append((lang.id, lang.language)) or result,Language.objects.all(), [])

    language = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=LANGUAGE_OPTIONS, label='언어')