# -*- coding: utf8 -*-

from django.conf.urls import url, include
from .import views

app_name = 'users'
urlpatterns = [
        url(r'^register/$', views.register, name = 'register'),
        url(r'^$', views.index, name = 'index'),
        url(r'^profile/(?P<pk>[0-9]+)/$', views.profile, name = 'profile'),
        ]


