from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.exceptions import ValidationError

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name product_count'.split()

 
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =Category
        fields = 'id name product_count'.split()


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=1, max_length=50)






class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model =Product
        fields = '__all__'


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=1, max_length=50)
    description= serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    category_id = serializers.IntegerField()

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category does not exist!')
        return category_id








class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model =Review
        fields = 'id text product stars'.split()


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required=False)
    product_id = serializers.IntegerField()
    stars = serializers.IntegerField(min_value=1, max_value=5, default=5)

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('Product does not exist!')
        return product_id
    





class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'title price category reviews rating'.split()
        depth = 1
