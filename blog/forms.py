from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('id','title', 'detail','pub_status', 'category')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'detail': CKEditorUploadingWidget(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'pub_status': forms.HiddenInput,
        }
