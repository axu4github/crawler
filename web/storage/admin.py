from django.contrib import admin
from models import Product, Price

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'unique', 'name', 'url', 'img', 'max_price', 'min_price', 'created', 'modified')


admin.site.register(Product, ProductAdmin)

class PriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'created', 'product_id')

admin.site.register(Price, PriceAdmin)
