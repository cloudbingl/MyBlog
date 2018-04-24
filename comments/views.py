from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from blog.models import Article
from .models import Comments
from .forms import CommentsForm
def add_comment(request, obj, form, user):
    if request.method == "POST":
        ct = ContentType.objects.get_for_model(obj)
        comment = Comments(content_type=ct,object_id=obj.pk)
        comment.user = user
        comment.save()
        cf = form(instance=comment)
