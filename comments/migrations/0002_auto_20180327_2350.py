# Generated by Django 2.0.2 on 2018-03-27 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'verbose_name': '评论', 'verbose_name_plural': '评论'},
        ),
    ]
