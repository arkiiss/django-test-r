from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.
class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M','Мужской'),
        ('F','Женский'),
    ]
    gender = models.CharField(
        max_length=1,
        choices = GENDER_CHOICES
    )

class Avatar(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        
    )
    image = models.BinaryField()