from django.urls import path
from . import views

urlpatterns = [
    path('<int:posto_id>/', views.analise_posto, name='analise_posto'),
    path('listar_vouchers/<int:posto_id>/', views.listar_vouchers_posto, name='listar_vouchers_posto'),
    path('registrar_gasto/<int:voucher_id>/', views.registrar_gasto, name='registrar_gasto'),
    path('escanear_voucher/<int:voucher_id>/', views.escanear_voucher, name='escanear_voucher'),
    path('validar_qrcode/<str:qrcode>/', views.validar_qrcode, name='validar_qrcode'),
    path('confirmacao/', views.confirmacao, name='confirmacao'),
    path('registrar_gasto_direto/<int:voucher_id>/', views.registrar_gasto_direto, name='registrar_gasto_direto'),
]
