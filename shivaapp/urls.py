from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
     path("",views.home,name="home"),
     path("send_otp",views.send_otp,name="send otp"),
     path('weather', views.weather, name='weather'),
     path('auth',views.auth,name='auth'),
     path('delete/<city_name>/', views.delete_city, name='delete_city'),
     path('logout',views.logoutUser,name='logout'),
      
]