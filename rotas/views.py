from django.shortcuts import render, redirect, get_object_or_404
from .models import Rota
from .forms import RotaForm

def cadastrar_rota(request):
    if request.method == 'POST':
        form = RotaForm(request.POST)
        if form.is_valid():
            rota = form.save(commit=False)
            rota.save()  # Salva a instância da rota para obter um ID
            form.save_m2m()  # Salva a relação ManyToMany após a rota ter sido salva
            rota.valor_total = rota.postos.count() * 10  # Calcula o valor total com base nos postos
            rota.save(update_fields=['valor_total'])  # Salva novamente para atualizar o valor total
            return redirect('listar_rotas')
    else:
        form = RotaForm()
    return render(request, 'rotas/cadastrar_rota.html', {'form': form})

def listar_rotas(request):
    rotas = Rota.objects.all()
    return render(request, 'rotas/listar_rotas.html', {'rotas': rotas})

def editar_rota(request, rota_id):
    rota = get_object_or_404(Rota, id=rota_id)
    if request.method == 'POST':
        form = RotaForm(request.POST, instance=rota)
        if form.is_valid():
            rota = form.save(commit=False)
            rota.save()  # Salva a rota para obter um ID
            form.save_m2m()  # Salva a relação ManyToMany
            rota.valor_total = rota.postos.count() * 10  # Calcula o valor total ao editar a rota
            rota.save(update_fields=['valor_total'])  # Salva novamente para atualizar o valor total
            return redirect('listar_rotas')
    else:
        form = RotaForm(instance=rota)
    return render(request, 'rotas/cadastrar_rota.html', {'form': form})

def deletar_rota(request, rota_id):
    rota = get_object_or_404(Rota, id=rota_id)
    rota.delete()
    return redirect('listar_rotas')
