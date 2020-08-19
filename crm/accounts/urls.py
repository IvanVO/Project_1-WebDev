from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [

    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),

    path('', views.home, name="index"),
    path('products/', views.products, name="products"), 
    path('customer/<str:pk>', views.customer, name="customer"),

    path('create_order/<str:pk>', views.create_order, name="create_order"),
    path('update_order/<str:pk>', views.update_order, name="update_order"),
    path('delete_order/<str:pk>', views.delete_order, name="delete_order"),
]
