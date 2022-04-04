from functools import reduce
from django import forms
from admin.models import Language

from admin.models import Language

class CompanyJoinForm(forms.Form):

    companyid = forms.CharField(
        error_messages={
            'required': '아이디를 입력해주세요.'
        },
        max_length=20, label='아이디'
    )

    
    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        max_length=256, label='비밀번호', widget=forms.PasswordInput
    )

    re_password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        max_length=256, label='비밀번호 확인', widget=forms.PasswordInput
    )

    name = forms.CharField(
        error_messages={
            'required': '회사 이름을 입력해주세요.'
        },
        max_length=15, label='회사 이름'
    )

    pic = forms.FileField(label='회사 사진')

    tel = forms.CharField(
        error_messages={
            'required': '전화번호를 입력해주세요.'
        },
        max_length=20, label='회사 전화번호'
    )

    email = forms.EmailField(
        error_messages={
            'required': '이메일을 입력해주세요.'
        },
        label='이메일'
    )

    address = forms.CharField(
        error_messages={
            'required': '주소를 입력해주세요.'
        },
        label='주소'
    )

    people = forms.IntegerField(
        error_messages={
        },
        required=False, label='직원 수'
    )

    url = forms.URLField(
        error_messages={
        },
        required=False, label='회사 홈페이지 URL'
    )

    summary = forms.CharField(
        error_messages={
        },
        required=False, label='회사소개', widget=forms.Textarea
    )

    category = forms.ChoiceField(
        choices=(('big','대기업'),('littlebig','중견기업'),('small','중소기업'),('start','스타트업')),
        label='회사 규모'
    )

    LANGUAGE_OPTIONS = reduce(lambda result, lang: result.append((lang.id, lang.language)) or result,Language.objects.all(), [])

    language = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=LANGUAGE_OPTIONS, label='사용 언어')

