from django.urls import path
from checkout import views


urlpatterns = [
    path('', views.checkout, name='checkout'),
    path(
        'checkout_succcess/<order_number>',
        views.checkout_success, name='checkout_success'),
]
