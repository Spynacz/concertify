# Generated by Django 4.2.11 on 2024-06-04 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_notification_hass_been_seen_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concertifyuser',
            name='picture',
            field=models.URLField(blank=True, null=True),
        ),
    ]
