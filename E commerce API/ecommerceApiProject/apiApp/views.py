from urllib import response
from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.response import Response


# Create your views here.


@api_view(['GET'])
def product_list(request):
    products=Product.objects.filter(featured=True)
    serializer=ProductListSerializers(products,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request,slug):
    product=Product.objects.get(slug=slug)
    serializer=ProductDetailSerializers(product)
    return Response(serializer.data)

@api_view(['GET'])
def category_list(request):
    catogories=Category.objects.all()
    serializer=CategoryListSerializers(catogories,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def category_detail(request,slug):
    category=Category.objects.get(slug=slug)
    serializer=CategoryDetailSerializers(category)
    return Response(serializer.data)