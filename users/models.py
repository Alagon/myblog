# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'pk': self.pk})

    class Meta(AbstractUser.Meta):
        pass
