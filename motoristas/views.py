import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuarios.decorators import group_required
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from vouchers.models import Voucher
from .models import Motorista
from .forms import MotoristaForm, LoginForm
from django.contrib.auth.decorators import login_required

# Variável global para armazenar senhas temporárias
motorista_senhas = {}

@login_required
@group_required('Administrador')
def cadastrar_motorista(request):
    if request.method == 'POST':
        form = MotoristaForm(request.POST)
        if form.is_valid():
            motorista = form.save()
            grupo_padrao, created = Group.objects.get_or_create(name='Motorista')
            senha = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            user = User.objects.create_user(username=motorista.cpf, password=senha)
            motorista_senhas[motorista.cpf] = senha  # Armazenar a senha temporariamente
            print(f'Senha gerada para {motorista.nome}: {senha}')
            return redirect('listar_motoristas')
    else:
        form = MotoristaForm()
    return render(request, 'motoristas/cadastrar_motorista.html', {'form': form})

@login_required
@group_required('Administrador')
def listar_motoristas(request):
    motoristas = Motorista.objects.all()
    # Criar uma lista de motoristas com suas senhas
    motoristas_com_senhas = [(motorista, motorista_senhas.get(motorista.cpf, '')) for motorista in motoristas]
    return render(request, 'motoristas/listar_motoristas.html', {'motoristas_com_senhas': motoristas_com_senhas})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            senha = form.cleaned_data['senha']
            user = authenticate(request, username=cpf, password=senha)
            if user is not None:
                login(request, user)
                return redirect('home_motorista')
            else:
                form.add_error(None, 'CPF ou senha inválidos')
    else:
        form = LoginForm()
    return render(request, 'motoristas/login.html', {'form': form})

@login_required
def home_motorista(request):
    motorista = Motorista.objects.get(cpf=request.user.username)
    vouchers = Voucher.objects.filter(motorista=motorista).exclude(status='Usado')
    return render(request, 'motoristas/home_motorista.html', {'motorista': motorista, 'vouchers': vouchers})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
@group_required('Administrador')
def gerar_senha_temporaria(request, cpf):
    senha = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    motorista = Motorista.objects.get(cpf=cpf)
    user = User.objects.get(username=cpf)
    user.set_password(senha)
    user.save()
    motorista_senhas[motorista.cpf] = senha
    return JsonResponse({'senha': senha})

@login_required
@group_required('Administrador')
def deletar_motorista(request, cpf):
    motorista = get_object_or_404(Motorista, cpf=cpf)
    user = User.objects.get(username=cpf)
    user.delete()
    motorista.delete()
    return redirect('listar_motoristas')
