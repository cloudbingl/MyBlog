from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'detail', 'category')
        widgets = {
            'detail': CKEditorUploadingWidget,
        }
