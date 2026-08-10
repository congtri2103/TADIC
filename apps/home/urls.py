from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ve-tadic/', views.ve_tadic, name='ve_tadic'),
    path('giai-phap/vroad-ai/', views.giai_phap_vroad, name='giai_phap_vroad'),
    path('tac-nhan-ai/', views.san_pham_list, name='tac_nhan_ai'),
    path('san-pham/', views.san_pham_list, name='san_pham_list'),
    path('san-pham/<slug:key>/', views.san_pham_detail, name='san_pham_detail'),
    path('du-an/', views.du_an_list, name='du_an'),
    path('tin-tuc/', views.tin_tuc_list, name='tin_tuc_list'),
    path('tin-tuc/<slug:slug>/', views.tin_tuc_detail, name='tin_tuc_detail'),
    path('lien-he/', views.lien_he, name='lien_he'),
]
