from django.urls import path
from bag import views


urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<product_id>/', views.add_to_bag, name='add_to_bag'),
    path('edit/<product_id>/', views.adjust_bag, name='adjust_bag'),
    path('delete/<product_id>/', views.delete_from_bag, name='delete_item'),
]
