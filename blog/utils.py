import datetime
from django.db.models import Q, Sum
from django.utils import timezone
from django.http.response import JsonResponse

from .models import Article, Category


def get_num_parginator(num, total_page, current_page):
    # 自定义分页，只显示5个页码
    if total_page < num:
        start_index = 1
        end_index = total_page + 1
    else:
        if current_page <= num // 2 + 1:
            start_index = 1
            end_index = num + 1
        else:
            start_index = current_page - num // 2
            end_index = current_page + num // 2 + 1
            if (current_page + num // 2) > total_page:
                end_index = total_page + 1
                start_index = total_page - num + 1
    return list(range(start_index, end_index))


def category_list_json_handle(request):
    """显示分类数据"""
    cate_ls = {}
    category_list = Category.objects.all()
    for cate in category_list:
        cate_ls[cate.id] = cate.name, cate.get_num()
    return JsonResponse(cate_ls)


def new_article_json_handle(request):
    """显示最新5篇文章"""
    article_ls = {}
    articles = Article.objects.filter(pub_status=True) \
                              .order_by('-pub_date')[0:5]
    for article in articles:
        article_ls[article.id] = article.title
    return JsonResponse(article_ls)


def hot_article_json_handle(request):
    """显示30天内5篇热门文章"""
    article_ls = {}
    today = timezone.now().date()
    thirty_day = today - datetime.timedelta(days=30)
    articles = Article.objects.filter(is_delete=False, pub_status=True)\
        .filter(Q(read_detail__date__lt=today)&Q(read_detail__date__gte=thirty_day)) \
        .annotate(read_num_sum=Sum('read_detail__read_num'))\
        .order_by('-read_num_sum')[:7]
    for a in articles:
        article_ls[str(a.id)] = a.title, a.get_read_num()
    return JsonResponse(article_ls)