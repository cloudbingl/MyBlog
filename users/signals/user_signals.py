from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from users.models import UserInfo
from sitemsg.models import Sitemsg,Notice



@receiver(post_save, sender=User, dispatch_uid="create_user")
def create_user_profile(sender, instance, created, **kwargs):
    """
    1. 创建用户时自动创建扩展信息
    2. 发送注册成功通知消息
    """
    if created:
        UserInfo.objects.create(user=instance)
        print("创建信号")
        Notice.objects.create(
            notice_user=instance,
            notice_title="注册成功",
            notice_detail="恭喜注册成功",
        )


@receiver(post_save, sender=User, dispatch_uid="save_user")
def save_user_profile(sender, instance, **kwargs):
    """
    用户更新信息时自动更新扩展信息
    """
    instance.userinfo.save()