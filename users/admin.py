from django.contrib import admin

from .models import UserInfo


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_email' ,'male', 'phone', 'qq']


admin.site.register(UserInfo, UserInfoAdmin)
