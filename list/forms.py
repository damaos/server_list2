# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
import re
from django.contrib.auth.models import User, Group
from .models import Server, Client, Asignacion, Interface, Platform, AsignacionCliente, Maestra
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm




STATUS_TYPE = (
    (True, 'Activo'),
    (False, 'Inactivo'),
)

class ServerForm(forms.ModelForm):

    class Meta:
        model = Server  
        fields = ['name', 'tipe', 'num_interface',  'virtual', 'platform', 'system_operative', 'model', 'service', 'city', 'seat', 'rack', 'observation' ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control '}),
            'tipe': forms.TextInput(attrs={'class': 'form-control '}),
            'num_interface': forms.TextInput(attrs={'class': 'form-control '}),
            'platform': forms.Select(attrs={'class': 'form-control '}),
            'system_operative': forms.TextInput(attrs={'class': 'form-control '}),
            'model': forms.TextInput(attrs={'class': 'form-control '}),
            'service': forms.TextInput(attrs={'class': 'form-control '}),
            'city': forms.TextInput(attrs={'class': 'form-control '}),
            'seat': forms.TextInput(attrs={'class': 'form-control '}),
            'rack': forms.TextInput(attrs={'class': 'form-control '}),
            'observation': forms.Textarea(attrs={'class': 'form-control ', 'rows': 4,  }),
        }




class AsignacionForm(forms.ModelForm):

    class Meta:
        model = Asignacion
        fields = ['server','interface',] 
        widgets = { 
             'server': forms.Select(attrs={'class': 'form-control '}),
             'interface': forms.Select(attrs={'class': 'form-control '}),

         }

class ClientForm(forms.ModelForm):
    
    class Meta:
        
        model = Client
        fields = [ 'name','phone','email' ]
        widgets = { 
             'name': forms.TextInput(attrs={'class': 'form-control '}),
             'phone': forms.TextInput(attrs={'class': 'form-control '}),
             'email': forms.TextInput(attrs={'class': 'form-control '}),
         }

class InterfaceForm(forms.ModelForm):
    
    class Meta:
        model = Interface
        fields = ['name_interface','ip', 'port', 'is_asignada'] 
        widgets = { 
            'name_interface': forms.TextInput(attrs={'class': 'form-control '}),
            'ip': forms.TextInput(attrs={'class': 'form-control '}),  
            'port': forms.TextInput(attrs={'class': 'form-control '}),      
         }

class PlatformForm(forms.ModelForm):
    
    class Meta:
        model = Platform
        fields = ['name_platform',] 
        widgets = { 
             'name_platform': forms.TextInput(attrs={'class': 'form-control '}),
             
         }


class ServerEditForm(forms.ModelForm):
    
    class Meta:
        model = Server  
        fields = ['name', 'tipe', 'num_interface',  'virtual', 'platform', 'system_operative', 'model', 'service', 'city', 'seat', 'rack', 'observation', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control '}),
            'tipe': forms.TextInput(attrs={'class': 'form-control '}),
            'num_interface': forms.TextInput(attrs={'class': 'form-control '}),
            'platform': forms.Select(attrs={'class': 'form-control '}),
            'system_operative': forms.TextInput(attrs={'class': 'form-control '}),
            'model': forms.TextInput(attrs={'class': 'form-control '}),
            'service': forms.TextInput(attrs={'class': 'form-control '}),
            'city': forms.TextInput(attrs={'class': 'form-control '}),
            'seat': forms.TextInput(attrs={'class': 'form-control '}),
            'rack': forms.TextInput(attrs={'class': 'form-control '}),
            'observation': forms.Textarea(attrs={'class': 'form-control ', 'rows': 4,  }),
        }        


class AsignacionClienteForm(forms.ModelForm):
    
    class Meta:
        model = AsignacionCliente
        fields = ['server', 'client'] 
        widgets = { 
             'server': forms.Select(attrs={'class': 'form-control '}),
             'client': forms.Select(attrs={'class': 'form-control '}),
         }


class MaestraForm(forms.ModelForm):
    
    class Meta:
        model = Maestra
        fields = ['server', 'client', 'asignacion', 'asignacionclient', 'platform', 'interface']


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=140, required=True)
    last_name = forms.CharField(max_length=140, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )




