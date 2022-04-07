from functools import reduce
from xml.etree.ElementTree import Comment
from django import forms
from admin.models import Language

from board.models import Board

class Boardform(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'developer', 'contents', 'language']

    # 언어
    LANGUAGE_OPTIONS = reduce(lambda result, lang: result.append((lang.id, lang.language)) or result, Language.objects.all(), [])

    language = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=LANGUAGE_OPTIONS, label='언어 선택')
        
    # 파일
    img = forms.FileField(label='파일')

    def clean(self):
        cleand_data = super().clean()

        print(cleand_data.items())

        self.title = cleand_data.get('title')
        self.developer = cleand_data.get('developer')
        self.contents = cleand_data.get('contents')
        self.language = cleand_data.get('language')

