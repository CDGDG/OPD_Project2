from xml.etree.ElementTree import Comment
from django import forms

from board.models import Board

class Boardform(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'developer', 'contents']

        

    # 파일
    img = forms.FileField(label='파일')

    def clean(self):
        cleand_data = super().clean()

        print(cleand_data.items())

        self.title = cleand_data.get('title')
        self.developer = cleand_data.get('developer')
        self.contents = cleand_data.get('contents')

