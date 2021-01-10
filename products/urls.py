from django.urls import path
from products import views


urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>', views.product_detail, name='product_detail'),
    path('category_search', views.category_search, name='category_search'),
    path('query_search', views.query_search, name='query_search'),
    path('store_management', views.store_management, name='store_management'),
    path('product_delete/<int:product_id>',
         views.product_delete, name='product_delete'),
    path('product_update/<int:product_id>',
         views.product_update, name='product_update'),
]
