# Generated by Django 2.2.4 on 2020-06-12 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comments',
        ),
        migrations.AddField(
            model_name='post',
            name='comments',
            field=models.IntegerField(default=0),
        ),
    ]
