from django.contrib.auth.models import AbstractUser
from django.db import models

class UserType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    matricula = models.CharField(max_length=20, unique=True)
    user_types = models.ManyToManyField(UserType, related_name='users')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if UserType.objects.filter(name='Administrador').exists():
            admin_type = UserType.objects.get(name='Administrador')
            if admin_type in self.user_types.all():
                self.is_staff = True
                self.is_superuser = True
            else:
                self.is_staff = False
                self.is_superuser = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
