from django.contrib import admin
from .models import Article, Category, Comment


# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'get_read_num' , 'category', 'pub_date', 'modify_date']
    ordering = ['pub_date']
    search_fields = ['title']
    list_per_page = 10
    fieldsets = [
        ('标题', {'fields': ['title']}),
        ('内容', {'fields': ['detail']}),
        ('分类', {'fields': ['category']}),
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'user', 'cmt_date']


admin.site.register(Category)
