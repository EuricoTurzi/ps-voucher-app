from django.shortcuts import render, redirect, get_object_or_404
from .models import Posto
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .forms import PostoForm

@login_required
def cadastrar_posto(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    if request.method == 'POST':
        form = PostoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_postos')
    else:
        form = PostoForm()
    return render(request, 'postos/cadastrar_posto.html', {'form': form})

@login_required
def listar_postos(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    postos = Posto.objects.all()
    return render(request, 'postos/listar_postos.html', {'postos': postos})

@login_required
def editar_posto(request, posto_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    posto = get_object_or_404(Posto, id=posto_id)
    if request.method == 'POST':
        form = PostoForm(request.POST, instance=posto)
        if form.is_valid():
            form.save()
            return redirect('listar_postos')
    else:
        form = PostoForm(instance=posto)
    return render(request, 'postos/editar_posto.html', {'form': form})

@login_required
def deletar_posto(request, posto_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    posto = get_object_or_404(Posto, id=posto_id)
    posto.delete()
    return redirect('listar_postos')