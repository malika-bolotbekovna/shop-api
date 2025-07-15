from rest_framework import serializers
from .models import Category, Product, Review

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

 
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =Category
        fields = 'name product_count'.split()



class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model =Product
        fields = 'id title price category'.split()



class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model =Review
        fields = 'id text product stars'.split()


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'title price category reviews rating'.split()
        depth = 1
