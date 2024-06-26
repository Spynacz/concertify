# Generated by Django 4.2.11 on 2024-04-15 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts_comments', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='commentvote',
            constraint=models.UniqueConstraint(fields=('comment', 'user'), name='unique_comment_user_combination'),
        ),
        migrations.AddConstraint(
            model_name='postvote',
            constraint=models.UniqueConstraint(fields=('post', 'user'), name='unique_post_user_combination'),
        ),
    ]
