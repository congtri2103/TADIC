from django.urls import path

from . import views

urlpatterns = [
    path('', views.van_ban_list, name='van_ban_list'),
    path('api/', views.van_ban_api, name='van_ban_api'),
]
