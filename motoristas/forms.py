# motoristas/forms.py
from django import forms
from django.contrib.auth.models import User, Group
from .models import Motorista
import random
import string

class LoginForm(forms.Form):
    cpf = forms.CharField(max_length=11)
    senha = forms.CharField(widget=forms.PasswordInput)

class MotoristaForm(forms.ModelForm):
    class Meta:
        model = Motorista
        fields = ['nome', 'cpf', 'placa_veiculo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'placa_veiculo': forms.TextInput(attrs={'class': 'form-control'}),
        }