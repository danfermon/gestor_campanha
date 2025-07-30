from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuarios(AbstractUser):
   # Foto de perfil
   foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

   # Nível do usuário
   NIVEIS = [
        ('1', 'Administrador'),
        ('2', 'Usuário Comum'),
        ('3', 'Visitante'),
    ]
   nivel = models.CharField(max_length=1, choices=NIVEIS, blank=True, null=True)

   def __str__(self):
      return self.username