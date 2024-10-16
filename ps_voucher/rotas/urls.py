from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_rota, name='cadastrar_rota'),
    path('', views.listar_rotas, name='listar_rotas'),
    path('editar/<int:rota_id>/', views.editar_rota, name='editar_rota'),
    path('deletar/<int:rota_id>/', views.deletar_rota, name='deletar_rota'),
]
