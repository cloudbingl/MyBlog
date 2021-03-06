# Generated by Django 2.0.2 on 2018-03-28 10:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20180327_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='at_user',
            field=models.CharField(default=0, max_length=32, verbose_name='回复用户'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comments',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='已删除?'),
        ),
        migrations.AddField(
            model_name='comments',
            name='quote_text',
            field=models.TextField(default=1, verbose_name='引用评论内容'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comments',
            name='comment_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='评论时间'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='text',
            field=models.TextField(verbose_name='评论内容'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='评论用户'),
        ),
    ]
