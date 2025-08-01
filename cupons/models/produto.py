from django.db import models
from .cupom import Cupom

class Produto(models.Model):
    cupom = models.ForeignKey(Cupom, on_delete=models.CASCADE, related_name='produtos')
    nome = models.CharField(max_length=255)
    quantidade = models.PositiveIntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    num_sorte = models.CharField(max_length=60)  

    def valor_total(self):
        return self.quantidade * self.valor_unitario

    def __str__(self):
        return f"{self.nome} x{self.quantidade}"
