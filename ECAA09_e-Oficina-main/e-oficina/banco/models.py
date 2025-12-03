from django.db import models
from django.contrib.auth.models import User

class Servico(models.Model):
    carro = models.CharField(max_length=100)
    imagem = models.TextField()
    tipo = models.CharField(max_length=20)


class SolicitacaoReparo(models.Model):
    """
    Modelo para solicitações de reparo enviadas por clientes
    """
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aceito', 'Aceito'),
        ('em_progresso', 'Em Progresso'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]
    
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitacoes_reparo')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    veiculo = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-data_criacao']
        verbose_name = "Solicitação de Reparo"
        verbose_name_plural = "Solicitações de Reparo"
    
    def __str__(self):
        return f"{self.titulo} - {self.cliente.username}"


class ImagemReparo(models.Model):
    """
    Modelo para armazenar imagens de reparos
    """
    solicitacao = models.ForeignKey(SolicitacaoReparo, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='reparos/%Y/%m/%d/')
    descricao = models.CharField(max_length=255, blank=True)
    data_upload = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-data_upload']
        verbose_name = "Imagem de Reparo"
        verbose_name_plural = "Imagens de Reparo"
    
    def __str__(self):
        return f"Imagem - {self.solicitacao.titulo}"


class InteresseSolicitacao(models.Model):
    """
    Modelo para armazenar quando uma oficina se interessa por uma solicitação
    """
    solicitacao = models.ForeignKey(SolicitacaoReparo, on_delete=models.CASCADE, related_name='interesses')
    escritorio = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interesses_solicitacoes')
    orcamento = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    descricao_proposta = models.TextField(blank=True)
    data_interesse = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-data_interesse']
        verbose_name = "Interesse em Solicitação"
        verbose_name_plural = "Interesses em Solicitações"
        unique_together = ('solicitacao', 'escritorio')
    
    def __str__(self):
        return f"{self.escritorio.username} interessado em {self.solicitacao.titulo}"