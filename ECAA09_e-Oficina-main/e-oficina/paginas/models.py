from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    """
    Modelo que estende o usuário padrão do Django
    para adicionar informações de tipo (Cliente ou Escritório)
    """
    TIPO_CHOICES = [
        ('cliente', 'Cliente'),
        ('escritorio', 'Escritório'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_display()}"
    
    class Meta:
        verbose_name = "Perfil de Usuário"
        verbose_name_plural = "Perfis de Usuários"
