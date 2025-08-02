from rest_framework import serializers
from .models import *




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