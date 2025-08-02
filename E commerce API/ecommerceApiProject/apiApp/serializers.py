from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

class ProductListSerializers(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields=["id","name","slug","image","price"]


class ProductDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields=["id","name","description","slug","image","price"]

class CategoryListSerializers(serializers.ModelSerializer):
    products=ProductListSerializers(many=True,read_only=True)
    class Meta:
        model=Category
        fields=["id","name","image","slug"]

class CategoryDetailSerializers(serializers.ModelSerializer):
    products=ProductListSerializers(many=True,read_only=True)
    class Meta:
        model=Category
        fields=["id","name","image","products"]

class CartItemSerializer(serializers.ModelSerializer):
    product=ProductListSerializers(read_only=True)
    sub_total=serializers.SerializerMethodField()
    class Meta:
        model=CartItem
        fields=["id","product","quantity","sub_total"]
    def get_sub_total(self,cartitem):
        total = cartitem.product.price = cartitem.quantity
        return total

    

class CartSerializer(serializers.ModelSerializer):
    cartitems=CartItemSerializer(read_only=True,many=True)
    cart_total=serializers.SerializerMethodField()
    class Meta:
        model=Cart
        fields=["id","cart_code","cartitems","cart_total"]

    def get_cart_total(self,cart):
        items=cart.cartitems.all()
        total=sum([item.quantity * item.product.price for item in items])
        return total
    

class CartStatSerializer(serializers.ModelSerializer):
    total_quantity=serializers.SerializerMethodField()
    class Meta:
        model=Cart
        fields=["id","cart_code","total_quantity"]


    def get_total_quantity(self,cart):
        items=cart.cartitems.all()
        total=sum([item.quantity  for item in items])
        return total
    


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        feilds=["id","first_name","last_name","profile_picture_url"]



class ReviewSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Review
        fields=["id","user","rating","review","reated","updated"]
