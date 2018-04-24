from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField

from read_statistics.models import ReadNumExtendMethod,ReadDetail,ReadNum


class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name="分类名称")

    def __str__(self):
        return self.name

    def get_num(self):
        num = Article.objects.filter(category=self.pk).count()
        return num

    class Meta:
        verbose_name = "文章分类"
        verbose_name_plural = verbose_name


class Article(models.Model, ReadNumExtendMethod):
    title = models.CharField(max_length=128, verbose_name="文章标题")
    detail = RichTextUploadingField(verbose_name="文章内容")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name="作者")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    pub_status = models.BooleanField(default=True, verbose_name="发布状态")
    modify_date = models.DateTimeField(auto_now=True, verbose_name="最后修改时间")
    comment_cout = models.IntegerField(default=0, verbose_name="评论数量")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name="文章分类")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")
    read_detail = GenericRelation(ReadDetail, related_query_name='articles')

    def __str__(self):
        return self.title

    '''
    # 此方法将使用新的APP来进行统计数据
        def get_read_num(self):
            """获取阅读量"""
            try:
                return self.readnum.read_num
            except exceptions.ObjectDoesNotExist as e:
                return 0
    '''

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ("-pub_date",)

    '''
    # 此模型已经单独创建APP
    class ReadNum(models.Model):
        read_num = models.IntegerField(default=0, verbose_name="阅读量")
        article = models.OneToOneField(Article, on_delete=models.CASCADE)
    '''


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                verbose_name="评论文章")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name="评论用户")
    reply_info = models.CharField(max_length=128, default="",
                                  verbose_name="回复信息")
    quote_info = models.TextField(default="", verbose_name="引用内容")
    comment = models.TextField(verbose_name="评论内容")
    cmt_date = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name
