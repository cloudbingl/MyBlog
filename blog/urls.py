from django.urls import path, re_path

from . import views
from . import utils

urlpatterns = [
    path('', views.index, name='index'),
    # 文章查看
    path('articles/', views.articles, name='articles'),
    re_path(r'^article/(?P<pk>\d+)/$', views.article, name='article'),

    # 文章增删改 和 文章管理
    path('edit_article/', views.edit_article, name='edit_article'),
    path('del_article/', views.del_article, name='del_article'),
    path('user_articles/', views.user_articles, name='user_articles'),
    # 后端验证文章表单
    path('check_article/', views.check_article_handle),

    # 按分类查看文章
    re_path(r'^filter_category/(?P<pk>\d+)/$', views.filter_category,
            name='filter_category'),
    # 按用户查看，查看用户分类
    re_path(r'^user/(?P<pk>\d+)/$', views.user_index, name='user_index'),

    # 评价添加和删除
    path(r'add_comment/', views.add_comment, name='add_comment'),
    re_path(r'^del_comment/(?P<pk>\d+)/$', views.del_comment_json_handle,
            name='del_comment'),
    path(r'user_comment/', views.user_comment, name='user_comment'),

    # 获取json数据
    # 获取分类json数据
    path('category_list_handle/', utils.category_list_json_handle),
    # 获取最新文章分类
    path('new_article_json_handle/', utils.new_article_json_handle),
    # 获取热门文章分类
    path('hot_article_json_handle/', utils.hot_article_json_handle),

]
app_name = 'blog'

handler404 = views.page_not_found
handler500 = views.page_error
from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
