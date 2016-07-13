# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Product(models.Model):

    unique = models.CharField(blank=False, null=False,
                              max_length=100, help_text='唯一标识')
    name = models.CharField(blank=False, null=False,
                            max_length=1000, help_text='名称')
    url = models.CharField(blank=False, null=False,
                           max_length=1000, help_text='详情连接')
    img = models.CharField(blank=False, null=False,
                           max_length=1000, help_text='图片连接')
    provider = models.CharField(
        blank=False, null=False, default='', max_length=100, help_text='供应商')
    max_price = models.FloatField(
        blank=False, null=False, default=0, help_text='最高价格')
    min_price = models.FloatField(
        blank=False, null=False, default=0, help_text='最低价格')
    created = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    modified = models.DateTimeField(auto_now=True, help_text='修改时间')

    class Meta:
        ordering = ('-modified',)


class Price(models.Model):

    product = models.ForeignKey(Product)
    price = models.FloatField(blank=False, null=False, help_text='价格')
    created = models.DateTimeField(auto_now=True, help_text='创建时间')

    class Meta:
        ordering = ('-created',)
