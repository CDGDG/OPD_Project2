from functools import reduce
from django import forms

from board.models import Board

class Boardform(forms.Form):
    #제목
    title = forms.CharField(
        error_messages={
            'required' : '제목을 입력해주세요'
        },
        max_length=20, label='제목'
    )

    # 작성자
    developer = forms.CharField(
        error_messages={
            "required": '작성자를 입력해주세요'
        },
        max_length=10, label='작성자'
    )

    # 내용
    contents = forms.CharField(
        error_messages={
            'required' : '내용을 입력해주세요'
        },
        widget=forms.Textarea, label="내용"
    )

    # 파일
    img = forms.FileField(label='파일')

