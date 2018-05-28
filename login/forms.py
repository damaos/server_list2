# -*- coding: utf-8 -*-
'''
Módulo de formulario del app login
'''
from django import forms


class LoginForm(forms.Form):
    '''
    Clase de formulario del app login
    '''
    username = forms.CharField(label='Nombre de usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    
    fields = ['username','password']
    widgets = {
            'username': forms.TextInput(attrs={'maxlength':30, 'minlength':4,'class': 'form-control','name': 'username'}),
            'password': forms.TextInput(attrs={'maxlength':30, 'minlength':4,'class': 'form-control','name': 'password'})
            
        }