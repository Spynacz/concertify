# Generated by Django 4.2.11 on 2024-03-30 15:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='title')),
                ('desc', models.CharField(max_length=300, verbose_name='description')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(verbose_name='social media link')),
                ('platform', models.CharField(choices=[('X', 'x'), ('INSTAGRAM', 'instagram'), ('FACEBOOK', 'facebook')], verbose_name='social media platform')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_media', to='events.event')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[(3, 'owner'), (2, 'moderator'), (1, 'staff'), (0, 'user')], verbose_name='role name')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='role', to='events.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='role', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='phone number')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_contact', to='events.event')),
            ],
        ),
        migrations.AddConstraint(
            model_name='socialmedia',
            constraint=models.UniqueConstraint(fields=('event', 'link'), name='unique_event_link_combination'),
        ),
        migrations.AddConstraint(
            model_name='role',
            constraint=models.UniqueConstraint(fields=('event', 'user'), name='unique_event_user_combination'),
        ),
    ]
