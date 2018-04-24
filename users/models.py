from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserInfo(models.Model):
    """用户扩展信息"""
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name="用户")
    male = models.BooleanField(default=True, verbose_name="男?")
    phone = models.CharField(max_length=11, default=0, blank=True,
                             verbose_name="联系电话")
    birth = models.DateField(blank=True, null=True, verbose_name="生日")
    qq = models.CharField(max_length=15, default=0, blank=True,
                          verbose_name="QQ")

    def get_email(self):
        return self.user.email

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "用户信息扩展"
        verbose_name_plural = verbose_name
