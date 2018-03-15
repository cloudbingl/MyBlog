from django.db import models
from django.contrib.auth.models import User

class Sitemsg(models.Model):
    """用户站内信"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="发送人")
    msg_title = models.CharField(max_length=128, verbose_name="标题")
    msg_detail = models.TextField(verbose_name="内容")
    recv_user = models.CharField(max_length=128, verbose_name="接收人")
    send_date= models.DateTimeField(auto_now_add=True, verbose_name="发送时间")
    msg_status = models.BooleanField(default=False, verbose_name="已读")
    is_delete =  models.BooleanField(default=False, verbose_name="是否删除")

    def __str__(self):
        return  self.msg_title

    class Meta:
        verbose_name = "站内信"
        verbose_name_plural = verbose_name

class Notice(models.Model):
    """系统通知"""
    notice_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="接收人")
    notice_title = models.CharField(max_length=128, verbose_name="公告标题")
    notice_detail = models.TextField(verbose_name="公告内容")
    notice_date = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    notice_status = models.BooleanField(default=True, verbose_name="发布状态")
    is_delete = models.BooleanField(default=False,verbose_name="是否删除")

    def __str__(self):
        return self.notice_title

    class Meta:
        verbose_name = "系统通知"
        verbose_name_plural = verbose_name