''' Serialisers.py'''
# from django.contrib.auth.models import User, Group
from shop.models import Category, SubCategory, Product
from rest_framework import serializers


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    subcategory = serializers.CharField(source='subcategory.id')
    class Meta:
        model = Product
        fields = ('__all__')         

class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer(many=True, read_only=True)
    category = serializers.CharField(source='category.id')    
    class Meta:
        model = SubCategory
        fields = ('name', 'image')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    subcategory = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ('name')