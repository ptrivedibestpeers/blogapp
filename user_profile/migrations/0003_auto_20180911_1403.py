# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-11 14:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_auto_20180907_0617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile_detail',
            name='profile_image',
            field=models.ImageField(default='default_image.png', upload_to='image_uploads/'),
        ),
    ]