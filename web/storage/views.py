from django.shortcuts import render
from storage.serializers import ProductSerializer, PriceSerializer
from storage.models import Product, Price
from rest_framework import viewsets

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    """docstring for QueryViewSet"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    


# class PriceViewSet(viewsets.ModelViewSet):
#     """docstring for QueryViewSet"""

#     queryset = Price.objects.all()
#     serializer_class = PriceSerializer