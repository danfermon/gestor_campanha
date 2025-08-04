from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

# para a parte da API
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.models import Token # para autenticação de APIs

from participantes.api_views import ParticipantesViewSet
from participantes.api_views import BuscarParticipantePorCelularView


router = DefaultRouter()
router.register(r'participantes', ParticipantesViewSet)



urlpatterns = [
    path('usuarios/', include('usuarios.urls')),
    path('participantes/', include('participantes.urls')),
    path('cupons/', include('cupons.urls')),
    path('skus_validos/', include('skus_validos.urls')),

    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/participantes/buscar-por-celular/', BuscarParticipantePorCelularView.as_view()),

    path('api/', include(router.urls)),

    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # configuração de midias - Danny - 26-06-2025

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
