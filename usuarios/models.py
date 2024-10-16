from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=50, choices=[('PA', 'PA'), ('Gerente', 'Gerente'), ('Administrador', 'Administrador')])

    def __str__(self):
        return self.user.username

# Conectar sinal para criar ou atualizar perfil
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Verificar se o perfil existe antes de salvar
    try:
        instance.perfil.save()
    except Perfil.DoesNotExist:
        Perfil.objects.create(user=instance)
