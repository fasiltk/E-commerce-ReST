from urllib import response
from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.contrib.auth import get_user_model


# Create your views here.
User=get_user_model()

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

@api_view(['POST'])
def add_to_cart(request):
    cart_code=request.data.get("cart_code")
    product_id=request.data.get("product_id")

    cart,created=Cart.objects.get_or_create(cart_code=cart_code)
    product=Product.objects.get(id=product_id)
    cartitem,created=CartItem.objects.get_or_create(product=product,cart=cart)
    cartitem.quantity=1
    cartitem.save()
    serializer=CartSerializer(cart)
    return Response(serializer.data)


@api_view(['PUT'])
def update_cartitem_quantity(request):
    cartitem_id=request.data.get("item_id")
    quantity=request.data.get("quantity")
    quantity=int(quantity)
    cartitem=CartItem.objects.get(id=cartitem_id)
    cartitem.quantity=quantity
    cartitem.save()

    serializer=CartItemSerializer(cartitem)
    return Response({"data":serializer.data,"message":"Cartitem uploaded successfullly"})


@api_view(['POST'])
def add_review(request):
    product_id=request.data.get("product_id")
    email=request.data.get("email")
    rating=request.data.get("rating")
    review_text=request.data.get("review")

    product=Product.objects.get(id=product_id)
    user=User.objects.get(email=email)
    review=Review.objects.create(product=product,user=user,rating=rating,review=review_text)
    serializer=ReviewSerializer(review)
    return Response(serializer.data)