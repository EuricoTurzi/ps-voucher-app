from django.shortcuts import render, redirect, get_object_or_404
from .models import Posto
from .forms import PostoForm

def cadastrar_posto(request):
    if request.method == 'POST':
        form = PostoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_postos')
    else:
        form = PostoForm()
    return render(request, 'postos/cadastrar_posto.html', {'form': form})

def listar_postos(request):
    postos = Posto.objects.all()
    return render(request, 'postos/listar_postos.html', {'postos': postos})

def editar_posto(request, posto_id):
    posto = get_object_or_404(Posto, id=posto_id)
    if request.method == 'POST':
        form = PostoForm(request.POST, instance=posto)
        if form.is_valid():
            form.save()
            return redirect('listar_postos')
    else:
        form = PostoForm(instance=posto)
    return render(request, 'postos/editar_posto.html', {'form': form})

def deletar_posto(request, posto_id):
    posto = get_object_or_404(Posto, id=posto_id)
    posto.delete()
    return redirect('listar_postos')
