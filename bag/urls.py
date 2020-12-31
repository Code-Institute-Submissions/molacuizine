from django.urls import path
from bag import views
# from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
]
