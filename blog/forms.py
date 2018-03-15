from django import forms

from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'detail', 'category']
        labels = {
            'title': '标题',
            'detail': '内容',
            'category': '分类',
        }