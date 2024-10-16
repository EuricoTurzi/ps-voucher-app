from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login_usuario'),
    path('logout/', views.logout_view, name='logout'),
    path('home/pa/', views.home_pa, name='home_pa'),
    path('home/gerente/', views.home_gerente, name='home_gerente'),
    path('home/admin/', views.home_admin, name='home_admin'),
    path('redirect_home/', views.redirect_home, name='redirect_home'),  # Adicionar a URL de redirecionamento
]
