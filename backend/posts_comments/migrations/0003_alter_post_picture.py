# Generated by Django 4.2.11 on 2024-06-04 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts_comments', '0002_commentvote_unique_comment_user_combination_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='picture',
            field=models.URLField(blank=True, null=True, verbose_name='picture'),
        ),
    ]
