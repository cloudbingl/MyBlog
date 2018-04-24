import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from .models import ReadNum
from .models import ReadDetail


def set_read_key(request, obj):
    """
    1. 查看cookie是否有已阅读过的标记，如果没有，执行阅读计数
    2. 获取文章是否有阅读记录，如果有+1，如果没有创建阅读计数对象并+1
    :param request:
    :param obj:
    :return:
    """
    ct = ContentType.objects.get_for_model(obj)
    cookie_key = '{}_{}_read'.format(ct.model, obj.id)
    if not request.COOKIES.get(cookie_key):
        # 总阅读数+1
        read_num, created = ReadNum.objects.get_or_create(content_type=ct,
                                                          object_id=obj.pk)
        read_num.read_num += 1
        read_num.save()

        # 每日阅读量详情
        date = timezone.now().date()
        read_detail, created = ReadDetail.objects.get_or_create(
            content_type=ct, object_id=obj.pk, date=date)
        read_detail.read_num += 1
        read_detail.save()
    return cookie_key


def get_seven_days_read_data(content_type):
    read_nums = []
    dates = []
    today = timezone.now().date()
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type,
                                                 date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates,read_nums


def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by("-read_num")
    return read_details[:5]

def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by("-read_num")
    return read_details[:5]

# def get_seven_days_hot_data(content_type):
#     today = timezone.now().date()
#     seven_days = today - datetime.timedelta(days=7)在·
#     read_details = ReadDetail.objects\
#                              .filter(content_type=content_type,
#                                      date__lt=today,
#                                      date__gte=seven_days) \
#                              .values("content_type", "object_id") \
#                              .annotate(read_num_sum=Sum('read_num')) \
#                              .order_by("-read_num_sum")
#     return read_details[:7]

def get_seven_days_hot_data():
    today = timezone.now().date()
    seven_day = today - datetime.timedelta(days=7)
    from blog.models import Article
    from django.db.models import Q
    articles = Article.objects.filter(Q(read_detail__date__lt=today) & \
                                      Q(read_detail__date__gte=seven_day)) \
                               .values('id', 'title')  \
                               .annotate(read_num_sum=Sum('read_detail__read_num')) \
                               .order_by('-read_num_sum')
    return articles[:7]