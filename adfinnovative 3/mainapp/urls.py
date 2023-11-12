from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    path('register',views.register, name= "register"),
    path('login',views.login, name= "login"),
    path('login_home',views.login_home.as_view(), name= "home"),
    path("otp",views.Otp, name= "otp"),
    path("cart",views.cart_page.as_view(), name= "cart"),
    path("orderConfirmed", views.orderConfirmed.as_view(), name= "orderConfirmed"),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
]