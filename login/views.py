# -*- coding: utf-8 -*-
from __future__ import unicode_literals
'''
Módulo de vistas del app login
'''
import re

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View, TemplateView
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import ugettext as _
from django.template.loader import get_template
from django.template.context import Context
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from .forms import UserForm, User, LoginForm, UserEditForm
from .models import UserProfile

from hashlib import sha1    
from random import random
from datetime import datetime, timedelta
import urllib
import json

#  Clase para iniciar sesion
class Viewlogin(View):
    


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


class UsersListView(View):
    '''
    logica del modulo de usuarios
    '''

    template_name = 'users/list_users.html'

    @method_decorator(login_required(login_url='/login/logout'))
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        metodo que permite la visualización de formularios al cargar la pagina de usuarios
        '''

        request.session.set_expiry(settings.SESSION_TIMEOUT)
        form = UserForm()

        return render(request, self.template_name, {
            'form': form,
        })
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        '''
        metodo que permite en registro de información de los usuarios del aplicativo
        '''

        request.session.set_expiry(settings.SESSION_TIMEOUT)
        form = UserForm(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form
            })
        username = form.cleaned_data['username']
        url = settings.URL_CECOS
        paramet = '[ "first_name", "last_name", "surname","email"]'
        params = urllib.parse.urlencode({
            'user': username,
            'fields': paramet
        }).encode(encoding='utf_8')

        try:
            try:
                response = urllib.request.urlopen(url, params).read()
            except Exception as e:
                messages.error(
                    request, 'No se obtuvo información con el usuario indicado.')
                return render(request, self.template_name, {
                    'form': form
                })
            response = json.loads(response.decode())
            user = User()
            user.first_name = response['epersonal']['first_name']
            user.last_name = response['epersonal']['last_name'] + \
                ' ' + response['epersonal']['surname']
            user.username = username
            user.is_active = True
            user.email = response['epersonal']['email']
            user.save()

            my_group = Group.objects.get(id=request.POST.get('profile'))
            my_group.user_set.add(user)

            messages.success(
                request, 'Se ha registrado el usuario correctamente.')
            return HttpResponseRedirect(reverse('list:user'))

        except Exception as e:
            messages.error(request, 'Por favor intente mas tarde.')
            return render(request, self.template_name, {
                'form': form,
            })


class UserEditView(View):
    '''
    logica de edicion de usuarios
    '''

    template_name = 'users/edit_users.html'
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        metodo que permite la visualización del formulario de edicion de la información del usuario seleccionado
        '''
        try:
            user_edit = User.objects.get(pk=kwargs['id'])
            form = UserEditForm(instance=user_edit)
            value = user_edit.groups.all()[0].id
            return render(request, self.template_name, {
                'form': form,
                'value':value,
            })
        except Exception as e:
            messages.error(request, 'No se encuentra un ID valido')
            return HttpResponseRedirect(reverse('login:user'))
    def post(self, request, *args, **kwargs):
        '''
        Método post
        '''

        user_edit = User.objects.get(pk=kwargs['id'])
        user = User.objects.get(username=request.user)
        form = UserEditForm(request.POST, instance=user_edit)
        old_group = user_edit.groups.first()

        if form.is_valid():
            new_group = Group.objects.get(name=form.cleaned_data['profile'])
            user = form.save()
            if old_group != new_group:
                user.groups.remove(old_group)
                user.groups.add(new_group)
                user.save()
            output = {
                'form': form,
                'success_message': 'Se ha actualizado el usuario ' + str(user_edit) + ' correctamente.',
            }
            return render(request, self.template_name, output)
        else:
            output = {
                'form': form
            }
            messages.warning(request, "Valide los errores.")
            return render(request, self.template_name, output)

