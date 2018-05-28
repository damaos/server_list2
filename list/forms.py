from django import forms
from .models import Server, Client, Asignacion, Interface, Platform

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
        fields = ['server','interface','client'] 
        widgets = { 
             'server': forms.Select(attrs={'class': 'form-control '}),
             'interface': forms.Select(attrs={'class': 'form-control '}),
             'client': forms.Select(attrs={'class': 'form-control '}),
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
        fields = ['name_interface', 'is_asignada'] 
        widgets = { 
             'name_interface': forms.TextInput(attrs={'class': 'form-control '}),
            
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