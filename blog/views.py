from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from blog import models
from blog.forms import ArticleForm
from blog.utils import get_num_parginator
from read_statistics.utils import set_read_key
from read_statistics.utils import get_seven_days_read_data
from read_statistics.utils import get_today_hot_data
from read_statistics.utils import get_yesterday_hot_data
from read_statistics.utils import get_seven_days_hot_data


def page_not_found(request):
    """404页面"""
    render(request, '404.html')


def page_error(request):
    """500页面"""
    render(request, '500.html')


def index(request):
    """主页"""
    context = {}
    num = models.Category.objects.get(id=1)
    print(num.get_num())
    article_content_type = ContentType.objects.get_for_model(models.Article)
    dates, read_nums = get_seven_days_read_data(article_content_type)
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(article_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(
        article_content_type)
    context['seven_days_hot_data'] = get_seven_days_hot_data()
    return render(request, 'blog/index.html', context)


def filter_category(request, pk):
    """查看单个分类内的文章"""
    context = {}
    try:
        cate = models.Category.objects.get(id=pk)
    except models.Category.DoesNotExist:
        return HttpResponseRedirect(reverse('blog:index'))
    articles = models.Article.objects.filter(category=cate.id, pub_status=True)

    page = request.GET.get('page')
    data_paginator = Paginator(articles, 10)
    data = data_paginator.get_page(page)
    context['articles'] = data

    # 自定义分页范围
    current_page = data.number
    total_page = data_paginator.num_pages
    my_page_range = get_num_parginator(5, total_page, current_page)
    context['my_page_range'] = my_page_range
    return render(request, 'blog/articles_filter.html', context)


# @cache_page(60 * 15)
def articles(request):
    """文章列表"""
    context = {}
    articles = models.Article.objects.filter(pub_status=True).order_by(
        '-pub_date')

    data_paginator = Paginator(articles, 10)
    page = request.GET.get('page')
    data = data_paginator.get_page(page)
    context['articles'] = data

    # 自定义分页范围
    current_page = data.number
    total_page = data_paginator.num_pages
    my_page_range = get_num_parginator(5, total_page, current_page)
    context['my_page_range'] = my_page_range
    return render(request, 'blog/articles.html', context)



def article(request, pk=None):
    """文章内容"""
    context = {}
    if request.method == 'GET':
        article = get_object_or_404(models.Article, pk=pk)
        # 如果是已经发表的文章，记录文章阅读次数
        if article.pub_status:
            comments = models.Comment.objects.filter(article=pk,
                                                     is_delete=False)
            # 阅读计数
            read_cookie_key = set_read_key(request, article)

            context['comments'] = comments
            context['article'] = article
            response = render(request, 'blog/article_detail.html', context)
            response.set_cookie(read_cookie_key, "1")
            return response
        else:
            messages.warning(request, "访问的文章不存在")
            return render(request, 'blog/articles.html')


@login_required
def edit_article(request, pk):
    """修改文章"""
    context = {}
    if request.user.is_authenticated:
        user = request.user

        if request.method == "GET":
            article = models.Article.objects.get(author=user, pk=pk)
            context['form'] = ArticleForm(instance=article)
            context['article'] = article
            return render(request, 'blog/article_edit.html', context)

        if request.method == "POST":
            form = ArticleForm(request.POST)
            if form.is_valid():
                print(form)
                models.Article.objects.filter(pk=pk).update(
                    **form.cleaned_data)
                messages.success(request, "文章修改成功")
                return HttpResponseRedirect(reverse('blog:user_articles'))


@login_required
def add_article(request):
    """添加新文章"""
    context = {}
    if request.user.is_authenticated:
        user = request.user

        if request.method == "GET":
            context['form'] = ArticleForm()
            return render(request, 'blog/article_add.html', context)

        if request.method == "POST":
            form = ArticleForm(request.POST)
            if form.is_valid():
                form_obj = form.save(commit=False)
                form_obj.author = user
                form.save()
                messages.success(request, '文章添加成功')
                return HttpResponseRedirect(reverse('blog:articles'))

@login_required
def del_article(request):
    """删除文章"""
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            del_id = request.POST.get('del_id', '')
            try:
                models.Article.objects.get(id=del_id, author=user).delete()
            except models.Article.DoesNotExist:
                messages.warning(request, '文章不存在')
            return HttpResponseRedirect(reverse('blog:user_articles'))


def user_index(request, pk):
    """用户首页"""
    context = {}
    try:
        user = User.objects.get(id=pk)
        context['user_info'] = user
    except User.DoesNotExist:
        messages.warning(request, '用户不存在')
        return render(request, 'blog/index.html')
    articles = models.Article.objects.filter(author=user, pub_status=True) \
                                     .order_by('-pub_date')
    context['articles'] = articles
    return render(request, 'users/user_index.html', context)


@login_required
def user_articles(request):
    """用户文章列表"""
    context = {}
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'GET':
            articles = models.Article.objects.filter(author=user) \
                                             .order_by('-pub_date')
            page = request.GET.get('page')
            data_paginator = Paginator(articles, 5)
            data = data_paginator.get_page(page)
            context['articles'] = data

            # 自定义分页范围
            current_page = data.number
            total_page = data_paginator.num_pages
            my_page_range = get_num_parginator(5, total_page, current_page)
            context['my_page_range'] = my_page_range
            return render(request, 'users/user_articles.html', context)


@login_required
def user_comment(request):
    """用户评论过的文章"""
    context = {}
    if request.user.is_authenticated:
        user = request.user
        comments = models.Comment.objects.filter(user=user, is_delete=False) \
            .order_by('-cmt_date')
        page = request.GET.get('page', 1)
        data_paginator = Paginator(comments, 20)
        data = data_paginator.get_page(page)
        context['comments'] = data
        return render(request, 'users/user_comments.html', context)


def add_comment(request):
    if request.user.is_authenticated:
        user = request.user

        if request.method == "POST":
            pass

# @login_required
# @transaction.atomic()
# def add_comment(request):
#     """添加评论"""
#     if request.user.is_authenticated:
#         user = request.user
#
#         if request.method == 'POST':
#             article_id = request.POST.get('article_id')
#             try:
#                 # 查询该文章是否被删除
#                 article_obj = models.Article.objects.get(id=article_id)
#             except models.Article.DoesNotExist:
#                 messages.warning(request, '文章已删除，无法评论')
#                 return HttpResponseRedirect(reverse('blog:articles'))
#
#             # 创建事务节点
#             transaction_comment = transaction.savepoint()
#             comment = request.POST.get('comment')
#
#             import re
#             # 匹配回复的用户
#             re_user = re.compile(r'@(.*)\r')
#             reply_user = re_user.findall(comment)
#
#             # 匹配引用的内容
#             re_quote = re.compile(r'\[quote\]\r\n(.*?)\r\n\[\/quote\]', re.M)
#             reply_quote = re_quote.search(comment)
#
#             # 创建评论对象
#             comment_obj = models.Comment()
#             comment = comment.split('[/quote]')[-1]
#
#             # 判断是否回复用户(回复和引用都将出现：@用户名)
#             if not reply_user:
#                 comment_obj.reply_info = ''
#                 comment_obj.quote_info = ''
#             else:
#                 # 将匹配到的用户名存入，准备后续的通知
#                 reply_user_list = ','.join(set(reply_user))
#                 comment_obj.reply_info = reply_user_list
#
#                 at_user_msg_handle(article_obj, comment, reply_user_list)
#
#                 # 如果有引用内容，保存引用的内容
#                 if reply_quote:
#                     reply_quote = reply_quote.group(1)
#                     comment_obj.quote_info = reply_quote
#
#             # 被评论的文章
#             comment_obj.article = article_obj
#             # 评论的用户
#             comment_obj.user = user
#             # 除去引用之后的评论文字
#             comment_obj.comment = comment
#             comment_obj.save()
#
#             # 没有出现错误将提交事务
#             transaction.savepoint_commit(transaction_comment)
#             return HttpResponseRedirect(
#                 reverse('blog:article', args=[article_id]))


@login_required
def del_comment_json_handle(request, pk):
    """删除评论"""
    if request.user.is_authenticated:
        user = request.user
        try:
            comment = models.Comment.objects.get(id=pk, is_delete=False,
                                                 user=user)
        except models.Comment.DoesNotExist:
            messages.warning(request, '此条评论已删除')
            return JsonResponse({'status': 'error'})
        comment.is_delete = True
        comment.save()
        messages.success(request, '此条评论已成功删除')
        return JsonResponse({'status': 'ok'})