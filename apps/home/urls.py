from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ve-tadic/', views.ve_tadic, name='ve_tadic'),
    path(
        'giai-phap/vroad-ai/',
        RedirectView.as_view(pattern_name='san_pham_vroad', permanent=True),
    ),
    path('giai-phap/', views.giai_phap_list, name='giai_phap_list'),
    path('giai-phap/<slug:key>/', views.giai_phap_detail, name='giai_phap_detail'),
    path(
        'tac-nhan-ai/',
        RedirectView.as_view(pattern_name='giai_phap_list', permanent=True),
    ),
    path('san-pham/', views.san_pham_list, name='san_pham_list'),
    path('san-pham/vroad-ai/', views.san_pham_vroad, name='san_pham_vroad'),
    path('san-pham/<slug:key>/', views.san_pham_detail, name='san_pham_detail'),
    path('du-an/', views.du_an_list, name='du_an'),
    path('tin-tuc/', views.tin_tuc_list, name='tin_tuc_list'),
    path('tin-tuc/<slug:slug>/', views.tin_tuc_detail, name='tin_tuc_detail'),
    path('lien-he/', views.lien_he, name='lien_he'),
]
