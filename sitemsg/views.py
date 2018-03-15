from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, reverse

from sitemsg import models


def at_user_msg_handle(article_obj, comment, reply_user_list):
    """评论被@的自动系统通知"""
    user = User.objects.get(username="系统通知")
    for recv_user in reply_user_list.split(","):
        sitemsg_obj = models.Sitemsg()
        sitemsg_obj.user = user
        msg_title = user.username + " :在评论中@了你"
        sitemsg_obj.msg_title = msg_title

        # 消息内容
        sitemsg_obj.msg_detail = """
        {0}\r\n
        评论内容：
        {1}\r\n

        原文链接：http://127.0.0.1:8006/article/{2}/
        """.format(msg_title, comment, article_obj.id)
        sitemsg_obj.recv_user = recv_user
        sitemsg_obj.save()

@login_required
def notice(request):
    """系统消息收件箱"""
    context = {}
    user = request.user
    notices = models.Notice.objects.filter(notice_user=user)
    context['notices'] = notices
    return render(request, 'sitemsg/msg_notice.html', context)


@login_required
def outbox(request):
    """发件箱"""
    context = {}
    if request.user.is_authenticated:
        user = request.user.username
        outbox = models.Sitemsg.objects.filter(user__username=user)
        context['outbox'] = outbox
    return render(request, 'sitemsg/msg_outbox.html', context)


@login_required
def inbox(request):
    """收件箱"""
    context = {}
    if request.user.is_authenticated:
        user = request.user.username
        inbox = models.Sitemsg.objects.filter(recv_user=user, msg_status=True)
        context['inbox'] = inbox
    return render(request, 'sitemsg/msg_inbox.html', context)


@login_required
def msg_detail(request, pk):
    """站内信详细信息"""
    context = {}
    if request.user.is_authenticated:
        user = request.user.username
        try:
            msg = models.Sitemsg.objects.get(id=pk)

            # 判断该用户是否有查看该信件的权限(是否是发送人或者接收人)
            if msg.user.username == user or msg.recv_user == user:
                msg.msg_status = True
                msg.save()
                context['msg'] = msg
                return render(request, 'sitemsg/msg_detail.html', context)
            else:
                messages.warning(request, "404. 抱歉! 您访问的资源不存在!")
                return HttpResponseRedirect(reverse('sitemsg:index'))
        except models.Sitemsg.DoesNotExist:
            messages.warning(request, "404. 抱歉! 您访问的资源不存在!")
            return HttpResponseRedirect(reverse('sitemsg:inbox'))


@login_required
def send_msg(request, uname=None):
    """发送站内信"""
    context = {}
    if request.user.is_authenticated:
        user = request.user.username
        if request.method == "GET":
            if uname:
                context['msg_recv_user'] = uname
            return render(request, 'sitemsg/msg_send.html', context)

        elif request.method == "POST":
            msg_recv_user = request.POST.get("msg_recv_user")
            msg_title = request.POST.get("msg_title")
            msg_detail = request.POST.get("msg_detail")
            msg_obj = models.Sitemsg()
            msg_obj.user = User.objects.get(username=user)
            msg_obj.msg_title = msg_title
            msg_obj.msg_detail = msg_detail
            msg_obj.recv_user = msg_recv_user
            msg_obj.save()
            messages.success(request, "发送成功")
            return HttpResponseRedirect(reverse('sitemsg:outbox'))


@login_required
def del_msg(request, pk):
    """删除信件"""
    models.Sitemsg.objects.get(id=pk).delete()
    messages.success(request, "删除成功")
    return HttpResponseRedirect(reverse('sitemsg:inbox'))


@login_required
def unread(request):
    """查看未读信件"""
    context = {}
    if request.user.is_authenticated:
        user = request.user.username
        unread = models.Sitemsg.objects.filter(recv_user=user,
                                               msg_status=False)
        context['unread'] = unread
    return render(request, 'sitemsg/msg_unread.html', context)
