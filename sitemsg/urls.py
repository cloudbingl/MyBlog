from django.urls import path, re_path

from sitemsg import views


app_name = 'sitemsg'

urlpatterns = [
    # 站内信
    path('inbox/', views.inbox, name='inbox'),
    path('outbox/', views.outbox, name='outbox'),
    path('unread/', views.unread, name='unread'),
    path('notice/', views.notice, name='notice'),
    re_path(r'^send/$', views.send_msg, name='send_msg'),
    re_path(r'^send/(?P<uname>\w+)/$', views.send_msg, name='send_msg'),
    re_path(r'^msg/(?P<pk>\d+)/$', views.msg_detail, name='msg_detail'),
    re_path(r'^del/(?P<pk>\d+)/$', views.del_msg, name='del_msg'),
]
