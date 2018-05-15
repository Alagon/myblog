# -*- coding: utf8 -*-
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.utils.translation import ugettext, ugettext_lazy as _
from .models import User

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')

