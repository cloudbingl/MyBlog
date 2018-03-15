from django.http.response import JsonResponse
from django.contrib.contenttypes.models import ContentType

from . import models
from site_statistics.models import ReadNum


def category_list_json_handle(request):
    """
    显示分类数据
    :param request:
    :return:
    """
    cate_ls = {}
    category_list = models.Category.objects.all()
    for cate in category_list:
        cate_ls[cate.id] = cate.name, cate.article_set.all().count()
    return JsonResponse(cate_ls)


def new_article_json_handle(request):
    """
    显示最新5篇文章
    """
    article_ls = {}
    articles = models.Article.objects.filter(pub_status=True).order_by(
        '-pub_date')[0:5]
    for article in articles:
        article_ls[article.id] = article.title
    return JsonResponse(article_ls)


def hot_article_json_handle(request):
    """
    显示最热5篇文章
    """
    article_ls = {}
    ct = ContentType.objects.get_for_model(models.Article)
    readnum = ReadNum.objects.filter(content_type=ct).order_by('-read_num')[
              0:5]
    for a in readnum:
        article_ls[
            str(a.content_object.id)] = a.content_object.title, a.read_num
    return JsonResponse(article_ls)



