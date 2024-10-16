from django import forms

class RegistrarGastoForm(forms.Form):
    valor_gasto = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
