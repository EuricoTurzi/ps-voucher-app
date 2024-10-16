from django.db import models

class Posto(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    gerente = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True, blank=True)  # Gerente pode ser adicionado depois

    def __str__(self):
        return self.nome
