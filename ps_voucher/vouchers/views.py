from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse  # Adicione esta linha
from .models import Voucher
from .forms import VoucherForm

def gerar_voucher(request):
    if request.method == 'POST':
        form = VoucherForm(request.POST)
        if form.is_valid():
            voucher = form.save(commit=False)
            voucher.valor_restante = voucher.rota.valor_total  # Define o valor restante baseado na rota
            voucher.save()
            return redirect('listar_vouchers')
    else:
        form = VoucherForm()
    return render(request, 'vouchers/gerar_voucher.html', {'form': form})

def listar_vouchers(request):
    vouchers = Voucher.objects.all()
    return render(request, 'vouchers/listar_vouchers.html', {'vouchers': vouchers})

def validar_voucher(request, codigo):
    voucher = get_object_or_404(Voucher, codigo=codigo)
    if request.method == 'GET':
        if voucher.status == 'Usado':
            return JsonResponse({'status': 'error', 'message': 'Este voucher já foi utilizado.'})
        else:
            voucher.status = 'Ativo' if voucher.valor_restante > 0 else 'Usado'
            voucher.save()
            return JsonResponse({'status': 'success', 'message': 'Voucher validado com sucesso!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Método não permitido.'}, status=405)

def validar_qrcode_view(request):
    return render(request, 'vouchers/validar_voucher.html')
