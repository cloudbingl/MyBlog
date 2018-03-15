#### 开发环境
* Python 3.54
* Django 2.0
```
pip install django
pip install django-tinymce
pip install django-markdownx
pip install django-ckeditor
```

#### 功能介绍
* blog
    * 主页
    * 文章列表(全部显示、分类显示)
    * 查看文章
    * 文章管理(编辑、删除)
    * 评论文章(评论、回复、引用)
    * 评论管理
* sitemsg
    * 发件箱
    * 收件箱
    * 未读
    * 查看信件
* access_statistics
    * 统计
* user
    * 注册
    * 登录
    * 注销
    * 个人信息
    * 账户信息
    
#### templates文件说明
* base.html 基础模版
* header.html 顶部导航
* left_menu.html 左侧菜单
* right_menu.html 右侧菜单
* blog/
    * tags/
    * index.html 主页
    * articles.html 文章列表
    * articles_filter.html 分类文章列表
    * article_detail 文章详情
    * article_add.html 添加文章
    * article_edit.html 编辑文章
    * article_del.html 删除文章
    * user_index.html 用户主页
    * user_articles.html 用户文章管理
    * user_comments.html 用户评论管理
* sitemsg/
    * msg_inbox.html 收件箱
    * msg_outbox.html 发件箱
    * msg_detail.html 信件详情
    * msg_send.html 发送信息
    * msg_unread.html 未读信息
* users/
    * login.html 登录
    * register.html 注册
    * user_account.html 账户设置
    * user_info.html 用户信息设置