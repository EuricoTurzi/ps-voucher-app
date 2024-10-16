from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from .models import Perfil

def create_groups():
    # Grupos que queremos criar
    groups = ['PA', 'Gerente', 'Administrador']

    # Permissões para cada grupo
    permissions = {
        'PA': [],
        'Gerente': [],
        'Administrador': []
    }

    for group_name in groups:
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f'Grupo {group_name} criado com sucesso.')
        for perm in permissions[group_name]:
            group.permissions.add(perm)

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'tipo_usuario']
    list_filter = ['tipo_usuario']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
