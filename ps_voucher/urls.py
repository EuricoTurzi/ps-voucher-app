from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('motoristas/', include('motoristas.urls')),
    path('vouchers/', include('vouchers.urls')),
    path('postos/', include('postos.urls')),  # Adicione esta linha
    path('rotas/', include('rotas.urls')),  # Adicione esta linha
    path('usuarios/', include('usuarios.urls')),
    path('analise_posto/', include('analise_posto.urls')),  # Adiciona o novo app de análise
    path('accounts/', include('django.contrib.auth.urls')),  # Adiciona URLs de autenticação padrão do Django
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),  # Adiciona a URL da página inicial
]

if settings.DEBUG or settings.SERVE_MEDIA_IN_PROD:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)