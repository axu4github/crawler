# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-12 22:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0003_product_provider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateTimeField(auto_now_add=True, help_text='\u521b\u5efa\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='product',
            name='modified',
            field=models.DateTimeField(auto_now=True, help_text='\u4fee\u6539\u65f6\u95f4'),
        ),
    ]