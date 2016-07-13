from django.shortcuts import render
from storage.serializers import ProductSerializer, PriceSerializer
from storage.models import Product, Price
from rest_framework import viewsets
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


class PriceViewSet(viewsets.ModelViewSet):
    """docstring for QueryViewSet"""

    queryset = Price.objects.all()
    serializer_class = PriceSerializer

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        print vars(request)
        print request.data

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            product = Product.objects.get(
                unique=serializer.data['product']['unique'])
            if serializer.data['price'] > product.max_price:
                product.max_price = serializer.data['price']

            if serializer.data['price'] < product.min_price:
                product.min_price = serializer.data['price']

            product.save()
        except Product.DoesNotExist, e:
            serializer.data['product']['max_price'] = serializer.data['price']
            serializer.data['product']['min_price'] = serializer.data['price']
            print serializer.data['product']
            product = Product.objects.create(**serializer.data['product'])

        price = Price.objects.create(price=serializer.data['price'], product_id=product.id)

        return Response(serializer.data)
