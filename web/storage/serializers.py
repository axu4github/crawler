# -*- coding: UTF-8 -*-
from models import Product, Price
from rest_framework import serializers

class ProductSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Product

class PriceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Price