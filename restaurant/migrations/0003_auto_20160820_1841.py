# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-20 18:41
from __future__ import unicode_literals

from django.db import migrations, models
import restaurant.models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_auto_20160820_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderspecial',
            name='photo',
            field=models.ImageField(upload_to=restaurant.models.get_upload_file_name),
        ),
    ]