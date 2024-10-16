from django import forms
from .models import Posto
from django.contrib.auth.models import User

class PostoForm(forms.ModelForm):
    gerente = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Gerente'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Posto
        fields = ['nome', 'endereco', 'cidade', 'estado', 'gerente']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
        }
