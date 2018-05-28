# -*- coding: utf-8 -*-
'''
Módulo de vistas del app login
'''
import re

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View

from .forms import LoginForm


class Viewlogin(View):
    '''
    Clase que permite el inicio de sesión
    '''

    template_name = 'login/login.html'

    def get(self, request):
        '''
        Método get
        '''
        if request.user.is_authenticated():
            if request.user.has_perm('auth.add_user'):
                
                return HttpResponseRedirect(reverse('list:list'))
            return HttpResponseRedirect(reverse('list:list'))
        form = LoginForm()
        output = {
            'form': form
        }
        return render(request, self.template_name, output)

    def post(self, request):
        '''
        Método post
        '''
        form = LoginForm(request.POST)
        next_url = None
        user_validator = request.POST.get('username')
        pass_validator = request.POST.get('password')
        if user_validator == '' or pass_validator == '':
            messages.error(request, 'Los campos usuario y contraseña son obligatorios')
            output = {
            'form': form
            }
            return render(request, self.template_name, output)
                          
        if not re.match('^[a-z]+$', user_validator):
            messages.error(
                        request, 'El campo usuario solo permite letras minúsculas ')
            output = {
            'form': form
            }
            return render(request, self.template_name, output)
        if request.GET.get('next') and request.GET.get('next') != None:
            next_url = request.GET.get('next')
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            url = settings.URL_AUTHENTICATION
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            passpost = {'user': username, 'password': password}
            request_object = requests.post(url, headers=headers, data=passpost)
            if request_object.status_code == 200:
                try:
                    user = User.objects.get(username=username)
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    if user and user.is_active:
                        login(request, user)
                        request.session.set_expiry(settings.SESSION_TIMEOUT)
                        if next_url != None:
                            return HttpResponseRedirect(next_url)
                        if user.has_perm('users.add_profile'):
                            return HttpResponseRedirect(reverse('list:list'))
                        return HttpResponseRedirect(reverse('list:list'))
                    messages.warning(
                        request, 'El usuario no se encuentra activo')
                except ObjectDoesNotExist:
                    messages.warning(
                        request, 'El usuario no se encuentra registrado en el aplicativo')
            else:
                for item in request_object.json().values():
                    messages.warning(request, item.replace("password","contraseña"))
        output = {
            'form': form
        }
        return render(request, self.template_name, output)


class Logout(View):
    '''
    Clase para finalizar sesión.
    '''

    def get(self, request, *args, **kwargs):
        '''
        Método get
        '''
        logout(request)
        return HttpResponseRedirect(reverse('login:login'))