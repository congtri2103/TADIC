from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='career-login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='career-logout'),
    path('dashboard/', views.dashboard, name='career-dashboard'),

    # CMS: Products
    path('cms/products/', views.product_list, name='cms-product-list'),
    path('cms/products/add/', views.product_create, name='cms-product-create'),
    path('cms/products/<int:pk>/edit/', views.product_edit, name='cms-product-edit'),
    path('cms/products/<int:pk>/delete/', views.product_delete, name='cms-product-delete'),
    path('cms/products/<int:pk>/toggle/', views.product_toggle_active, name='cms-product-toggle'),

    # CMS: News
    path('cms/news/', views.news_list, name='cms-news-list'),
    path('cms/news/add/', views.news_create, name='cms-news-create'),
    path('cms/news/<int:pk>/edit/', views.news_edit, name='cms-news-edit'),
    path('cms/news/<int:pk>/delete/', views.news_delete, name='cms-news-delete'),
    path('cms/news/<int:pk>/toggle/', views.news_toggle_publish, name='cms-news-toggle'),

    # CMS: Projects
    path('cms/projects/', views.project_list, name='cms-project-list'),
    path('cms/projects/add/', views.project_create, name='cms-project-create'),
    path('cms/projects/<int:pk>/edit/', views.project_edit, name='cms-project-edit'),
    path('cms/projects/<int:pk>/delete/', views.project_delete, name='cms-project-delete'),
    path('cms/projects/<int:pk>/toggle/', views.project_toggle_active, name='cms-project-toggle'),

    # CMS: Contacts
    path('cms/contacts/', views.contact_list, name='cms-contact-list'),
    path('cms/contacts/<int:pk>/delete/', views.contact_delete, name='cms-contact-delete'),

    # CMS: Văn bản pháp luật
    path('cms/vanban/', views.vanban_list, name='cms-vanban-list'),
    path('cms/vanban/<int:pk>/toggle/', views.vanban_toggle_hien_thi, name='cms-vanban-toggle'),
    path('cms/vanban/<int:pk>/delete/', views.vanban_delete, name='cms-vanban-delete'),

    # User Management
    path('users/', views.user_list, name='user-list'),
    path('users/add/', views.user_create, name='user-create'),
    path('users/<int:pk>/edit/', views.user_edit, name='user-edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='user-delete'),
]
