# Generated by Django 4.2.3 on 2023-09-15 06:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_like_alter_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='unlike',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='like',
            field=models.ManyToManyField(related_name='liked_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
