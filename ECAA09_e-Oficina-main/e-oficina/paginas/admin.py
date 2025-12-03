from django.contrib import admin
from .models import PerfilUsuario


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'data_criacao')
    list_filter = ('tipo', 'data_criacao')
    search_fields = ('usuario__username', 'usuario__email')
    readonly_fields = ('data_criacao',)