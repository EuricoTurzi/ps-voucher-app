from django import forms
from .models import Voucher
from motoristas.models import Motorista
from rotas.models import Rota

class VoucherForm(forms.ModelForm):
    motorista = forms.ModelChoiceField(queryset=Motorista.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    rota = forms.ModelChoiceField(queryset=Rota.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Voucher
        fields = ['motorista', 'rota']
