# motoristas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_motorista, name='cadastrar_motorista'),
    path('', views.listar_motoristas, name='listar_motoristas'),
    path('login/', views.login_view, name='login_motorista'),
    path('home/', views.home_motorista, name='home_motorista'),  # Adicione esta linha
    path('logout/', views.logout_view, name='logout_motorista'),  # Adicione esta linha
    path('gerar_senha/<str:cpf>/', views.gerar_senha_temporaria, name='gerar_senha_temporaria'),  # Nova URL
    path('deletar/<str:cpf>/', views.deletar_motorista, name='deletar_motorista'),  # Nova URL
]
