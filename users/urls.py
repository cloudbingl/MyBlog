from django.urls import path

from users import views
from users import utils
app_name = 'users'

urlpatterns = [
    # 登录、注销和注册
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),

    # 用户信息
    path('index/', views.user_index, name='user_index'),
    path('user_info/', views.user_info, name='user_info'),


    path('user_account/', views.user_account, name='user_account'),
    # 修改密码
    path('update_password/', views.update_password, name='update_password'),

    path('check_username/', utils.check_username)
]
