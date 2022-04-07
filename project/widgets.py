from django.utils.safestring import mark_safe
from django import forms

class ImagePreviewWidget(forms.widgets.FileInput):
    def render(self, name, value, **kwargs):
        input_html = super().render(name, value, **kwargs)
        if value:
            img_html = mark_safe(f'<img src="{value.url}" id="thumbnail_preview" height="200" /><br><br>')
        else:
            img_html = mark_safe(f'<img src="" id="thumbnail_preview" height="200" /><br><br>')
        return f'{img_html}{input_html}'