from django.db import models
from postos.models import Posto

class Rota(models.Model):
    nome = models.CharField(max_length=100)
    postos = models.ManyToManyField(Posto)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Salva a instância da rota para obter um ID
        self.valor_total = self.postos.count() * 10  # Calcula o valor total com base nos postos
        super().save(update_fields=['valor_total'])  # Salva novamente para atualizar o valor total

    def __str__(self):
        return self.nome
