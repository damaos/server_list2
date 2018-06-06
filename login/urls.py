# -*- coding: utf-8 -*-
'''
Módulo de urls para el app de login
'''
from django.conf.urls import url

from .views import Viewlogin, Logout, UsersListView, UserEditView

urlpatterns = [
    url(r'^$', Viewlogin.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^users/$', UsersListView.as_view(), name='user'),
    url(r'^edit_user/(?P<id>\d+)/edit/$', UserEditView.as_view(), name='edit_user'),
    
]