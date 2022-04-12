from functools import reduce
from .models import Comment
from django import forms
from admin.models import Language
from board.models import Board
from project.widgets import ImagePreviewWidget

class Boardform(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'developer', 'contents','img', 'language']

    # developer = forms.CharField(label='작성자')
    # 언어
    LANGUAGE_OPTIONS = reduce(lambda result, lang: result.append((lang.id, lang.language)) or result,Language.objects.all(), [])

    language = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=LANGUAGE_OPTIONS, label='언어 선택')
        
    # 파일
    img = forms.FileField(allow_empty_file= True, label='파일', required=False)

    def clean(self):
        cleand_data = super().clean()


        self.title = cleand_data.get('title')
        self.developer = cleand_data.get('developer')
        self.contents = cleand_data.get('contents')
        self.language = cleand_data.get('language')

class BoardUpdateForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title','contents']

    # 언어
    LANGUAGE_OPTIONS = reduce(lambda result, lang: result.append((lang.id, lang.language)) or result,Language.objects.all(), [])
    
    language = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=LANGUAGE_OPTIONS, label='언어 선택')

    # 이미지


    def __init__(self, *args, **kwargs):
        super(BoardUpdateForm, self).__init__(*args, **kwargs)
        language = self.instance.language
        self.initial['language'] = [lang.id for lang in language.all()]


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = {'contents'}
