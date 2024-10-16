from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_posto, name='cadastrar_posto'),
    path('', views.listar_postos, name='listar_postos'),
    path('editar/<int:posto_id>/', views.editar_posto, name='editar_posto'),
    path('deletar/<int:posto_id>/', views.deletar_posto, name='deletar_posto'),
]
