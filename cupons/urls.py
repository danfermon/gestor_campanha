from django.urls import path
from django.http import HttpResponse
from . import views



urlpatterns = [
    #path('ler-qrcode/', views.ler_qrcode_view, name='ler_qrcode_view'),
    
    path('cupom/<int:id_participante>/', views.cadastrar_cupom, name='cadastrar_cupom'),
    path('salvar_qrcode/<int:id_participante>/', views.salvar_qrcode_ajax, name='salvar_qrcode_ajax'),
    path('cadastrar_cupom/<int:id_participante>/', views.cadastrar_cupom, name='cadastrar_cupom'),
    #path('cadastrar_cupom_qrcode/<int:id_participante>/', views.cadastrar_cupom_qrcode, name='cadastrar_cupom_qrcode'),
    
    
]