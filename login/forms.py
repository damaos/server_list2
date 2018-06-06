# -*- coding: utf-8 -*-
from __future__ import unicode_literals
'''
Módulo de formulario del app login
'''
from django import forms
from django.contrib.auth.models import User, Group
from django.forms import ModelForm
from django.utils.translation import ugettext as _
 

STATUS_TYPE = (
    (True, 'Activo'),
    (False, 'Inactivo'),
)

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


class UserForm(ModelForm):
    '''
    formularios para registro de usuarios
    '''
    
    username = forms.CharField(label="Usuario de red de emtelco", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control type-diarie', 'name': 'username'}),
                               error_messages={'invalid': 'Ingresa un usuario válido'})
    
    profile = forms.ModelChoiceField(queryset=Group.objects.all(), label = "Perfil de Usuario", widget=forms.Select)
    
    is_active = forms.ChoiceField(label = "Estado", required=False, widget=forms.Select, choices=STATUS_TYPE)
    


    class Meta:
        '''
        Contiene el modelo que necesita el template
        '''
        model = User
        fields = ['username','profile','first_name','last_name','is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','name': 'username'})
        }
         

class UserEditForm(UserForm):
    
    area = None
    
    def clean_first_name(self):
            
        first_name = self.cleaned_data.get('first_name')
            
        if not re.match('^[a-zA-Z-ñÑ-áéíóúÁÉÍÓÚ ]+$', first_name):
            raise forms.ValidationError('Sólo se permite letras')
            
        return first_name 
        
    def clean_last_name(self):
            
        last_name = self.cleaned_data.get('last_name')
            
        if not re.match('^[a-zA-Z-ñÑ-áéíóúÁÉÍÓÚ ]+$', last_name):
            raise forms.ValidationError('Sólo se permite letras')
            
        return last_name 
    
    area = forms.ChoiceField(label = "Dirección/Gerencia", required=False, widget=forms.Select)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['area'].choices = centrocostos()

    class Meta:
        '''
        Contiene el modelo que necesita el template
        '''
        model = User
        fields = ['username','first_name','last_name','profile','is_active']
        widgets = {
        }