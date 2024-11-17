from django.db import models
from postos.models import Posto

class Rota(models.Model):
    nome = models.CharField(max_length=100)
    postos = models.ManyToManyField(Posto)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=40.00)  # Define o valor padrão de R$40.00

    def save(self, *args, **kwargs):
        # Remove o cálculo dinâmico e define o valor_total fixo de R$40
        self.valor_total = 40.00
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
