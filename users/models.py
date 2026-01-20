from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from rolepermissions.roles import assign_role

class UserManager(BaseUserManager):
    def _create_user(self, email, username, perfil, vaga, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, perfil=perfil, vaga=vaga, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, perfil='basic', vaga=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, username, perfil, vaga, password, **extra_fields)

    def create_superuser(self, email, username, perfil='full', password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, username, perfil, vaga, password, **extra_fields)
        
class Users(AbstractUser):
    email = models.EmailField('E-mail', unique=True)
    vaga = models.CharField('Vaga', max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'vaga']

    choices_perfil = [
        ('', 'Selecione um perfil'),
        ('full', 'Administrador'),
        ('basic', 'Básico'),
    ]
    perfil = models.CharField(max_length=10, choices=choices_perfil)

    objects = UserManager()

    def __str__(self):  
        return self.email
