from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import RegistrarGastoForm
from .models import GastoVoucher
from postos.models import Posto
from vouchers.models import Voucher
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

@login_required
def analise_posto(request, posto_id):
    posto = get_object_or_404(Posto, id=posto_id)

    # Verificar se o usuário é o gerente do posto
    if request.user != posto.gerente:
        return render(request, 'erro_permissao.html')

    vouchers = Voucher.objects.filter(rota__postos=posto)
    gastos = GastoVoucher.objects.filter(posto=posto)
    valor_total_utilizado = sum(gasto.valor_gasto for gasto in gastos)

    context = {
        'posto': posto,
        'total_vouchers': vouchers.count(),
        'valor_total_utilizado': valor_total_utilizado,
    }

    return render(request, 'analise_posto/analise_posto.html', context)

@login_required
def listar_vouchers_posto(request, posto_id):
    posto = get_object_or_404(Posto, id=posto_id)
    
    # Verificar se o usuário é o gerente do posto
    if request.user != posto.gerente:
        return render(request, 'erro_permissao.html')

    vouchers = Voucher.objects.filter(rota__postos=posto)

    context = {
        'posto': posto,
        'vouchers': vouchers,
    }
    
    return render(request, 'analise_posto/listar_vouchers_posto.html', context)

@login_required
def registrar_gasto(request, voucher_id):
    voucher = get_object_or_404(Voucher, id=voucher_id)

    if request.method == 'POST':
        form = RegistrarGastoForm(request.POST)
        if form.is_valid():
            valor_gasto = form.cleaned_data['valor_gasto']
            request.session['valor_gasto'] = str(valor_gasto)  # Converte para string antes de salvar na sessão
            request.session['voucher_codigo'] = voucher.codigo  # Salva o código do voucher na sessão
            return redirect('escanear_voucher', voucher_id=voucher.id)
    else:
        form = RegistrarGastoForm()
    
    return render(request, 'analise_posto/registrar_gasto.html', {'form': form, 'voucher': voucher})

@login_required
def escanear_voucher(request, voucher_id):
    voucher = get_object_or_404(Voucher, id=voucher_id)
    valor_gasto = request.session.get('valor_gasto')
    voucher_codigo = request.session.get('voucher_codigo')

    if valor_gasto is not None:
        valor_gasto = Decimal(valor_gasto)  # Converte de volta para Decimal

    return render(request, 'analise_posto/escanear_voucher.html', {'voucher': voucher, 'valor_gasto': valor_gasto})

@login_required
def validar_qrcode(request, qrcode):
    voucher = get_object_or_404(Voucher, codigo=qrcode)
    valor_gasto = request.session.get('valor_gasto')
    voucher_codigo = request.session.get('voucher_codigo')
    gerente = request.user

    if valor_gasto is not None:
        valor_gasto = Decimal(valor_gasto)

    # Verificar se o gerente é responsável pelo posto específico
    postos_gerente = Posto.objects.filter(gerente=gerente)
    if not postos_gerente.exists():
        return JsonResponse({'status': 'error', 'message': 'Você não tem permissão para validar vouchers neste posto.'})

    logger.info(f"Validando QR Code: Voucher Código = {voucher.codigo}, Status = {voucher.status}, Valor Restante = {voucher.valor_restante}, Valor Gasto = {valor_gasto}")

    if voucher.codigo == voucher_codigo and voucher.status == 'Ativo' and voucher.valor_restante >= valor_gasto:
        voucher.valor_restante -= valor_gasto
        if voucher.valor_restante == 0:
            voucher.status = 'Usado'
        voucher.save(update_fields=['valor_restante', 'status'])
        
        # Registrar o gasto no posto
        for posto in postos_gerente:
            GastoVoucher.objects.create(voucher=voucher, posto=posto, valor_gasto=valor_gasto)

        voucher.refresh_from_db()
        logger.info(f"Voucher atualizado: Novo Valor Restante = {voucher.valor_restante}, Novo Status = {voucher.status}")
        return JsonResponse({'status': 'success', 'message': 'Voucher validado com sucesso!'})
    else:
        logger.error(f"Erro na validação do QR Code: QR Code inválido ou valor excede o restante do voucher.")
        return JsonResponse({'status': 'error', 'message': 'QR Code inválido ou valor excede o restante do voucher.'})

@login_required
def registrar_gasto_direto(request, voucher_id):
    voucher = get_object_or_404(Voucher, id=voucher_id)
    gerente = request.user

    # Verificar se o gerente é responsável pelo posto específico
    postos_gerente = Posto.objects.filter(gerente=gerente)

    if not postos_gerente.exists():
        return redirect('listar_vouchers_posto', posto_id=postos_gerente.first().id)

    if request.method == 'POST':
        form = RegistrarGastoForm(request.POST)
        if form.is_valid():
            valor_gasto = form.cleaned_data['valor_gasto']
            valor_gasto = Decimal(valor_gasto)

            print(f"Tentando registrar gasto: Voucher = {voucher.codigo}, Valor Gasto = {valor_gasto}, Valor Restante Antes = {voucher.valor_restante}")

            if voucher.status == 'Ativo' and voucher.valor_restante >= valor_gasto:
                voucher.valor_restante -= valor_gasto
                print(f"Novo Valor Restante (Antes de Salvar) = {voucher.valor_restante}")
                if voucher.valor_restante == 0:
                    voucher.status = 'Usado'
                else:
                    voucher.status = 'Ativo'
                voucher.save(update_fields=['valor_restante', 'status'])
                
                # Registrar o gasto no posto
                for posto in postos_gerente:
                    GastoVoucher.objects.create(voucher=voucher, posto=posto, valor_gasto=valor_gasto)

                voucher.refresh_from_db()
                print(f"Voucher atualizado: Novo Valor Restante (Após Salvar) = {voucher.valor_restante}, Novo Status = {voucher.status}")
                return redirect('listar_vouchers_posto', posto_id=postos_gerente.first().id)
            else:
                print(f"Erro ao validar o voucher: Valor Gasto = {valor_gasto}, Valor Restante = {voucher.valor_restante}")
                return redirect('listar_vouchers_posto', posto_id=postos_gerente.first().id)

    else:
        form = RegistrarGastoForm()
    
    return render(request, 'analise_posto/registrar_gasto_direto.html', {'form': form, 'voucher': voucher})

@login_required
def confirmacao(request):
    return render(request, 'analise_posto/confirmacao.html')
