from functools import reduce
from django import forms
from admin.models import Language
from project.models import Project
from project.widgets import ImagePreviewWidget

class Projectform(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'summary', 'contents', 'startdate', 'private', 'thumbnail', 'language']

    # 시작일
    startdate = forms.DateTimeField(label='시작일')

    # 언어
    LANGUAGE_OPTIONS = reduce(lambda result, lang: result.append((lang.id, lang.language)) or result,Language.objects.all(), [])

    language = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=LANGUAGE_OPTIONS, label='언어 선택')

    thumbnail = forms.ImageField(widget=ImagePreviewWidget, allow_empty_file= True)

    def clean(self):   
        # 우선 부모 Form 의 clean() 수행 --> 값이 들어있지 않으면 error 처리 
        cleand_data = super().clean()

        print(cleand_data.items())

        self.title = cleand_data.get('title')
        self.summary = cleand_data.get('summary')
        self.contents = cleand_data.get('contents')
        self.startdate = cleand_data.get('startdate')
        self.private = cleand_data.get('private')
        self.language = cleand_data.get('language')

        
class ProjectUpdateForm(forms.ModelForm):
    # 시작일
    startdate = forms.DateTimeField(label='시작일')
    # 종료일
    enddate = forms.DateTimeField(label='시작일', required=False)
    # 언어
    LANGUAGE_OPTIONS = reduce(lambda result, lang: result.append((lang.id, lang.language)) or result,Language.objects.all(), [])

    language = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=LANGUAGE_OPTIONS, label='언어 선택')

    thumbnail = forms.ImageField(widget=ImagePreviewWidget, allow_empty_file= True)

    class Meta:
        model = Project
        fields = ['title', 'summary', 'contents', 'startdate', 'enddate', 'private', 'thumbnail', 'language']

