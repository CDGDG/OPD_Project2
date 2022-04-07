from django.utils.safestring import mark_safe
from django import forms

class PicPreviewWidget(forms.widgets.FileInput):
    def render(self, name, value, **kwargs):
        input_html = super().render(name, value, **kwargs)
        if value:
            pic_html = mark_safe(
                f'<img src="{value.url}" id="pic_preview" height="200" /><br><br>')
            return f'{pic_html}{input_html}'
        return input_html

class ResumePreviewWidget(forms.widgets.FileInput):
    def render(self, name, value, **kwargs):
        input_html = super().render(name, value, **kwargs)
        if value:
            resume_html = mark_safe(
                f'<img src="{value.url}" id="resume_preview" height="200" /><br><br>')
            return f'{resume_html}{input_html}'
        return input_html