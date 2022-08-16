from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.

class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True, verbose_name='Аватар')
    github_profile = models.URLField(blank=True, null=True, verbose_name='Профиль на GitHub')
    description = models.TextField(blank=True, max_length=3000, null=True, verbose_name='О себе')
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile',
                                verbose_name='Пользователь')
