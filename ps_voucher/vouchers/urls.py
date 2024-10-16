# vouchers/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('gerar/', views.gerar_voucher, name='gerar_voucher'),
    path('', views.listar_vouchers, name='listar_vouchers'),
    path('validar/<str:codigo>/', views.validar_voucher, name='validar_voucher'),
    path('validar/', views.validar_qrcode_view, name='validar_voucher_view'),

]
