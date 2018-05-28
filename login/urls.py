# -*- coding: utf-8 -*-
'''
Módulo de urls para el app de login
'''
from django.conf.urls import url

from .views import Viewlogin, Logout

urlpatterns = [
    url(r'^$', Viewlogin.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
]