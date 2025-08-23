from django.contrib import admin
from django.urls import path, include
from product import views
from . import swagger


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/categories/<int:id>/', views.CategoryDetailAPIView.as_view()),
    path('api/v1/products/<int:id>/', views.ProductDetailAPIView.as_view()),
    path('api/v1/reviews/<int:id>/', views.ReviewViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('api/v1/categories/', views.CategoryListCreateAPIView.as_view()),
    path('api/v1/products/', views.ProductListCreateAPIView.as_view()),
    path('my-products/', views.OwnerProductListAPIView.as_view()),
    path('api/v1/reviews/', views.ReviewViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('api/v1/products/reviews/', views.product_review_api_view),
    path('api/v1/products/send-email/', views.SendProductsEmailAPIView.as_view()),
    path('api/v1/users/', include('users.urls'))
]

urlpatterns += swagger.urlpatterns
