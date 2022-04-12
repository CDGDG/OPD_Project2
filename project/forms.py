from functools import reduce
from django import forms
from admin.models import Language
from project.models import Project

class Projectform(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'summary', 'contents', 'thumbnail', 'startdate', 'private', 'language']

    # 언어
    LANGUAGE_OPTIONS = reduce(lambda result, lang: result.append((lang.id, lang.language)) or result,Language.objects.all(), [])

    language = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=LANGUAGE_OPTIONS, label='언어*')

    thumbnail = forms.ImageField(allow_empty_file= True, label="썸네일", required=False)

    startdate = forms.DateTimeField(widget=forms.DateInput(format=('%Y년 %m월 %d일'), attrs={'class': 'form-control', 'type':"date"}), label="시작일", required=False)

    def clean(self):   
        # 우선 부모 Form 의 clean() 수행 --> 값이 들어있지 않으면 error 처리 
        cleand_data = super().clean()
        
        self.title = cleand_data.get('title')
        self.summary = cleand_data.get('summary')
        self.contents = cleand_data.get('contents')
        self.startdate = cleand_data.get('startdate')
        self.private = cleand_data.get('private')
        self.language = cleand_data.get('language')

        
class ProjectUpdateForm(forms.ModelForm):
    # 시작일
    startdate = forms.DateTimeField(widget=forms.DateInput(attrs={'class': 'form-control', 'type':"date"}), label="시작일", required=False)
    # 종료일
    enddate = forms.DateTimeField(widget=forms.DateInput(attrs={'class': 'form-control', 'type':"date"}), label="종료일", required=False)
    # 언어
    LANGUAGE_OPTIONS = reduce(lambda result, lang: result.append((lang.id, lang.language)) or result,Language.objects.all(), [])

    language = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=LANGUAGE_OPTIONS, label='언어 선택')

    thumbnail = forms.ImageField(allow_empty_file= True, label="썸네일", required=False)


    class Meta:
        model = Project
        fields = ['title', 'summary', 'contents', 'thumbnail','startdate', 'enddate', 'private', 'language']

    def __init__(self, *args, **kwargs):
        super(ProjectUpdateForm, self).__init__(*args, **kwargs)
        language = self.instance.language
        self.initial['language'] = [lang.id for lang in language.all()]
