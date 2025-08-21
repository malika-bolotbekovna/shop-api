from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.http import Http404
from common.permissions import IsOwner, IsAnonymous, IsStaff
from common.validators import validate_age
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer
from .serializers import CategoryDetailSerializer, ProductDetailSerializer, ReviewDetailSerializer
from .serializers import ProductReviewSerializer, ProductValidateSerializer, CategoryValidateSerializer, ReviewValidateSerializer
from .models import Category, Product, Review






class ExceptionHandledAPIView(APIView):
    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            return Response(
                {'error': str(exc)},
                status=status.HTTP_404_NOT_FOUND
            )
        return super().handle_exception(exc)


class CustomPagination(PageNumberPagination):
    page_size = 5

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })





class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def post(self, request, *args, **kwargs):
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )
        name = serializer.validated_data.get('name')
        category = Category.objects.create(name=name)
        category.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data=CategoryDetailSerializer(category).data
        )


class CategoryDetailAPIView(ExceptionHandledAPIView, RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = 'id'
    
    def get_object(self):
        category_id = self.kwargs.get('id')
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise Http404(f'Category with id={category_id} does not exist!')
    
    
    def put(self, request, *args, **kwargs):
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
                )
        category = self.get_object()
        category.name = serializer.validated_data.get('name')
        category.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data=CategoryDetailSerializer(category).data
        )




class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    permission_classes = [IsOwner | IsAnonymous | IsStaff]

    
    def post(self, request, *args, **kwargs):
        validate_age(request.user.birthday)
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
                )
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category_id = serializer.validated_data.get('category_id')

        product = Product.objects.create(
            title=title,
            description=description,
            price=price,
            category_id=category_id,
            owner=request.user
        )
        product.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data=ProductDetailSerializer(product).data
        )

    
class ProductDetailAPIView(ExceptionHandledAPIView, RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'id'
    permission_classes = [IsOwner]

    def get_object(self):
        product_id = self.kwargs.get('id')
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise Http404(f'Product with id={product_id} does not exist!')
    
    
    def put(self, request, *args, **kwargs):
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
                )
        product = self.get_object()
        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.category_id = serializer.validated_data.get('category_id')
        product.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data=ProductDetailSerializer(product).data
        )


class OwnerProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user).select_related('category')


class ReviewViewSet(ExceptionHandledAPIView, ModelViewSet):
    queryset = Review.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return ReviewValidateSerializer
        elif self.action in ['retrieve']:
            return ReviewDetailSerializer
        return ReviewSerializer

    def get_object(self):
        review_id = self.kwargs.get('id')
        try:
            return Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            raise Http404(f'Review with id={review_id} does not exist!')
        

    def create(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review = Review.objects.create(**serializer.validated_data)
        return Response(
            ReviewDetailSerializer(review).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        for attr, value in serializer.validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return Response(
            ReviewDetailSerializer(instance).data,
            status=status.HTTP_201_CREATED
        )



@api_view(['GET'])
def product_review_api_view(request):
    products = Product.objects.all()
    data = ProductReviewSerializer(instance=products, many=True).data
    return Response(
        data=data,
        status=status.HTTP_200_OK
    )