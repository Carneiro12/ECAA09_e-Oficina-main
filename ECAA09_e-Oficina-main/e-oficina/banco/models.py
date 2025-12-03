from django.db import models

class Servico(models.Model):
    carro = models.CharField(max_length=100)
    imagem = models.TextField()
    tipo = models.CharField(max_length=20)