from django import forms
from .models import Rota

class RotaForm(forms.ModelForm):
    class Meta:
        model = Rota
        fields = ['nome', 'postos']
        widgets = {
            'postos': forms.CheckboxSelectMultiple(),
        }

    def clean(self):
        cleaned_data = super().clean()
        postos = cleaned_data.get('postos')
        if postos:
            cleaned_data['valor_total'] = len(postos) * 10  # Calcula o valor total com base nos postos
        return cleaned_data
