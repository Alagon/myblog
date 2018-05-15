# -*- coding: utf-8 -*-

from django import forms
from .models import Post

class PostPublishForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'tags', 'category', 'excerpt', 'author']
