from django.contrib.auth.models import AbstractUser
from django.db import models
from .usuario_manager import UsuarioManager
class Usuario(AbstractUser):
    username = None  # <--- REMOVE o campo username
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    is_paciente = models.BooleanField(default=False)
    is_nutricionista = models.BooleanField(default=False)

    objects = UsuarioManager() 