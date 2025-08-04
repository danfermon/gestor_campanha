from django.urls import path
from django.http import HttpResponse
from . import views



urlpatterns = [
    #path('ler-qrcode/', views.ler_qrcode_view, name='ler_qrcode_view'),
    
    path('cupom/<int:id_participante>/', views.cad_cupom, name='cad_cupom'),
    path('salvar_qrcode/<int:id_participante>/', views.salvar_qrcode_ajax, name='salvar_qrcode_ajax'),
    path('cad_cupom_codigo/<int:id_participante>/', views.cad_cupom_codigo, name='cad_cupom_codigo'),
    path('cadastrar_cupom_qrcode/<int:id_participante>/', views.cadastrar_cupom_qrcode, name='cadastrar_cupom_qrcode'),
    
    
]
