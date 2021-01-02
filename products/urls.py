from django.urls import path
from products import views


urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>', views.product_detail, name='product_detail'),
    path('category_search', views.category_search, name='category_search'),
]
