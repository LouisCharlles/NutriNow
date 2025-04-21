from django.contrib.auth.models import AbstractUser
from django.db import models
class Usuario(AbstractUser):
    is_paciente = models.BooleanField(default=False)
    is_nutricionista = models.BooleanField(default=False)