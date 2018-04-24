from django.contrib.auth import signals
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User


class Comments(models.Model):
    """评论模型"""
    # 关联ContentType
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField(verbose_name="评论内容")
    quote_text = models.TextField(default="", verbose_name="引用评论内容")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                             verbose_name="评论用户")
    at_user = models.CharField(max_length=32, verbose_name="回复用户")
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    is_delete = models.BooleanField(default=False, verbose_name="已删除?")

    events = GenericRelation('Event')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def cmt_notice(self):
        message = "{}发表了评论".format(self.user)
        return message


class Event(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def notice(self):
        return self.content_object.cmt_notice()


def comments_post_save(sender, instance, signal, *args, **kwargs):
    cmt = instance
    event = Event(user=cmt.user, content_object=cmt)
    event.save()

from django.db.models import signals
signals.post_save.connect(comments_post_save, sender=Comments)