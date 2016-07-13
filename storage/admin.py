# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Product, Price

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'unique', 'name', 'min_price', 'max_price', 'provider', 'url', 'img', 'created', 'modified')
    search_fields = ['name']


admin.site.register(Product, ProductAdmin)

class PriceAdmin(admin.ModelAdmin):
    def get_product_id(self, obj):
        return obj.product.id

    get_product_id.short_description = 'product'

    list_display = ('get_product_id', 'price', 'created')
    search_fields = ['product__id'] # '__' 表示关联对象搜索 

admin.site.register(Price, PriceAdmin)
