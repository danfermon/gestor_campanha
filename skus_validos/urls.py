from django.urls import path, include
from . import views

urlpatterns = [
    path('skus/', views.skus, name='skus'),
    path('importar_skus/', views.importar_skus, name='importar_skus'),

]