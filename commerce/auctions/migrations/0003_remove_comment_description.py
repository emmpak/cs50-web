# Generated by Django 3.1.5 on 2021-03-10 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_comment_listing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='description',
        ),
    ]