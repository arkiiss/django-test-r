from django.db import models
from django.contrib.auth.models import AbstractUser
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