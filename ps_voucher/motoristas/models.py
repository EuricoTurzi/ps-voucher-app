from django.db import models

class Motorista(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    placa_veiculo = models.CharField(max_length=7)

    def __str__(self):
        return self.nome
