from datetime import timedelta
from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse


def login(request):
    """用户登录"""
    content = {}
    if request.method == "GET":
        return render(request, "users/login.html", content)

    if request.method == "POST":
        login_name = request.POST.get("username", "").strip()
        login_pwd = request.POST.get("password", "").strip()
        next_url = request.POST.get("next_url", "").strip()
        save_name = request.POST.get("save_name", 0)
        user = authenticate(username=login_name, password=login_pwd)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "登陆成功")
            # request.session["username"] = login_name
            # 设置session过期时间为 关闭浏览器后过期
            # request.session.set_expiry(0)
            httprr = HttpResponseRedirect("/")
            if next_url:
                print(next_url)
                httprr = HttpResponseRedirect(next_url)
            print(next_url)
            return httprr
        else:
            messages.warning(request, "用户名或密码错误")
            return HttpResponseRedirect(reverse("user:login"))


@login_required
def logout(request):
    """注销"""
    if request.user.is_authenticated:
        next_url = request.GET.get("next")
        auth.logout(request)
        # messages.success(request, "注销成功")
        if next_url:
            print(next_url)
            return HttpResponseRedirect(next_url)
    return redirect("/")


def register(request):
    """用户注册"""
    content = {}
    if request.method == "GET":
        return render(request, 'users/register.html', content)
    elif request.method == "POST":
        username = request.POST.get("username").strip()
        pwd = request.POST.get("password").strip()
        repwd = request.POST.get("re_password").strip()
        email = request.POST.get("email").strip()
        auth_code = request.POST.get("auth_code").strip()

        if pwd == repwd:
            try:
                User.objects.get(username=username)
                messages.warning(request, "用户名已存在")
            except User.DoesNotExist:
                num = User.objects.filter(email=email).count()
                if num != 0:
                    messages.warning(request, "该邮箱已经注册")
                    return HttpResponseRedirect(reverse('user:register'))
                user = User.objects.create_user(username=username, email=email,
                                                password=pwd)
                user.save()
                # TODO 注册成功后登陆
                return HttpResponseRedirect(reverse('blog:articles'))
        return HttpResponseRedirect(reverse('user:register'))


@login_required
def user_info(request):
    """查看用户信息"""
    if request.user.is_authenticated:
        username = request.user.username

        if request.method == "GET":
            return render(request, 'users/user_info.html')

        if request.method == "POST":
            pass


@login_required
def user_account(request):
    return render(request, 'users/user_account.html')


@login_required
def update_password(request):
    """用户修改密码"""
    if request.user.is_authenticated:
        user = request.user.username

        if request.method == "GET":
            return render(request, 'users/user_account.html')

        elif request.method == "POST":
            old_password = request.POST.get("old_password").strip()
            new_password = request.POST.get("new_password").strip()
            re_new_password = request.POST.get("re_new_password").strip()

            # 再次对密码进行基本验证
            if new_password != re_new_password:
                messages.warning(request, "新密码两次输出不一致")
                return HttpResponseRedirect(reverse('user:user_account'))
            elif old_password == new_password:
                messages.warning(request, "新密码不能和当前密码一致")
                return HttpResponseRedirect(reverse('user:user_account'))

            # 对用户进行认证
            user_obj = authenticate(username=user, password=old_password)

            # 如果密码不正确返回修改密码页面
            if not user_obj:
                messages.warning(request, "原密码错误")
                return HttpResponseRedirect(reverse('user:user_account'))

            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request, "密码设置成功,请重新登录")
            auth.logout(request)
            return HttpResponseRedirect(reverse('user:login'))


def user_index(request):
    return render(request, 'users/user_index.html')
