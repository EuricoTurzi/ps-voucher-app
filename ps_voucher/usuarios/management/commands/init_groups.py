from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Cria grupos de usuários padrão'

    def handle(self, *args, **kwargs):
        grupos = ['PA', 'Gerente', 'Administrador']

        for grupo in grupos:
            Group.objects.get_or_create(name=grupo)
            self.stdout.write(self.style.SUCCESS(f'Grupo {grupo} garantido!'))
