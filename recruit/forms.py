from django import forms

from recruit.models import Recruit

class RecruitUpdateForm(forms.ModelForm):
    class Meta:
        model = Recruit
        fields = ['ing','title', 'contents',]