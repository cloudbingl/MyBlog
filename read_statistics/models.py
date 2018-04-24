from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.fields import exceptions
from django.utils import timezone


class ReadNum(models.Model):
    """阅读量计数"""
    read_num = models.IntegerField(default=0, verbose_name="阅读量")
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING,
                                     verbose_name="文章")
    object_id = models.PositiveIntegerField(verbose_name="对象ID")
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name= "阅读量"
        verbose_name_plural = verbose_name


class ReadNumExtendMethod(object):
    """扩展ReadNum的一些方法"""
    def get_read_num(self):
        ct = ContentType.objects.get_for_model(self)
        try:
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0


class ReadDetail(models.Model):
    """每一天的阅读记录"""
    date = models.DateField(default=timezone.now)
    read_num = models.IntegerField(default=0, verbose_name="当天阅读量")

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING,
                                     verbose_name="文章")
    object_id = models.PositiveIntegerField(verbose_name="对象ID")
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name= "每日阅读详情"
        verbose_name_plural = verbose_name
