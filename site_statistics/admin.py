from django.contrib import admin
from sitemsg.models import Sitemsg, Notice
from site_statistics.models import ReadNum, ReadDetail

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'content_object')

@admin.register(ReadDetail)
class ReadDetailAdmin(admin.ModelAdmin):
    list_display = ('date', 'read_num', 'content_object')