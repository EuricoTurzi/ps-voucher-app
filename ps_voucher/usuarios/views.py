from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistroUsuarioForm, LoginForm
from postos.models import Posto
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Adicionar o usuário a um grupo padrão
            grupo_padrao, created = Group.objects.get_or_create(name='Usuarios')
            user.groups.add(grupo_padrao)
            login(request, user)
            return redirect('home')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.groups.filter(name='PA').exists():
                    return redirect('home_pa')
                elif user.groups.filter(name='Gerente').exists():
                    return redirect('home_gerente')
                elif user.groups.filter(name='Administrador').exists():
                    return redirect('home_admin')
                else:
                    return redirect('home')
            else:
                form.add_error(None, 'Username ou senha inválidos')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    user = request.user
    if user.groups.filter(name='Gerente').exists():
        # Lógica para Gerente
        context = {
            'section': 'gerente'
        }
    elif user.groups.filter(name='PA').exists():
        # Lógica para PA
        context = {
            'section': 'pa'
        }
    elif user.groups.filter(name='Administrador').exists():
        # Lógica para Administrador
        context = {
            'section': 'administrador'
        }
    else:
        context = {
            'section': 'usuario'
        }
    return render(request, 'usuarios/home.html', context)

def atribuir_grupo(user, group_name):
    group, created = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)
    
def is_pa(user):
    return user.groups.filter(name='PA').exists()

def is_gerente(user):
    return user.groups.filter(name='Gerente').exists()

def is_admin(user):
    return user.groups.filter(name='Administrador').exists()

@login_required
@user_passes_test(is_pa)
def home_pa(request):
    return render(request, 'usuarios/home_pa.html')

@login_required
@user_passes_test(is_gerente)
def home_gerente(request):
    gerente = request.user
    postos = Posto.objects.filter(gerente=gerente)
    return render(request, 'usuarios/home_gerente.html', {'postos': postos})

@login_required
@user_passes_test(is_admin)
def home_admin(request):
    return render(request, 'usuarios/home_admin.html')

@login_required
def redirect_home(request):
    user = request.user
    if user.groups.filter(name='PA').exists():
        return redirect('home_pa')
    elif user.groups.filter(name='Gerente').exists():
        return redirect('home_gerente')
    elif user.groups.filter(name='Administrador').exists():
        return redirect('home_admin')
    else:
        return redirect('home')