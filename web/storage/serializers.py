# -*- coding: UTF-8 -*-
from models import Product, Price
from rest_framework import serializers


class ProductSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Product
        fields = ('unique', 'name', 'url', 'img', 'provider')


class PriceSerializer(serializers.HyperlinkedModelSerializer):

    product = ProductSerializer()

    class Meta:
        model = Price
        fields = ('product', 'price')
