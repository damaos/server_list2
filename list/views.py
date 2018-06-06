# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic.detail import DetailView
from django.core import serializers
from django.urls import reverse
from django.contrib.auth.models import Group
import re
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required


import urllib
import json



from .forms import ServerForm, AsignacionForm, ClientForm, PlatformForm, InterfaceForm, ServerEditForm, AsignacionClienteForm
from .models import Server, Asignacion, Client, Platform, Interface, AsignacionCliente 


 # vista que permite traer una lista de servidores 
class ServerList(ListView):
    
    template_name = 'servers/server_list.html'
    @method_decorator(login_required)
    def get(self, request):
        '''
        metodo get 
        '''
        query = request.GET.get("q")
        sort =  "activo"
        list_server = None
        if query:
            if query.lower().strip() == 'activo':
                list_server = Server.objects.filter(Q(is_active__icontains = 1))
            elif query.lower().strip() == 'inactivo':
                list_server = Server.objects.filter(Q(is_active__icontains = 0)) 
            else:      
                list_server = Server.objects.filter(
                    Q(name__icontains=query) |
                    Q(tipe__icontains=query) |
                    Q(num_interface__icontains=query) |
                    Q(virtual__icontains=query)|
                    Q(platform__name_platform__icontains=query)|
                    Q(system_operative__icontains=query)|
                    Q(model__icontains=query)|
                    Q(service__icontains=query)|
                    Q(city__icontains=query)|
                    Q(seat__icontains=query) |
                    Q(rack__icontains=query)     
            ).order_by('is_active')
        else:
            list_server = Server.objects.filter(is_active='True')
        page =request.GET.get("page")
        output = {
            'list_server': list_server
        }
        return render(request, self.template_name, output)


# clase para crear un nuevo servidor
class ServerNewView(View):
    '''
    Clase para crear un servidor
    '''
    template_name = 'servers/new_server.html'
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        Método get
        '''
        form = ServerForm()
        list_server = Server.objects.all()
        output = {
            'form': form,
            'list_server': list_server
        }
        return render(request, self.template_name, output)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        '''
        Método post
        '''
        
        form = ServerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')    

        output = {
            'form': form,
            'messages': "Revise los campos correctamente.",
        }
        
        return render(request, self.template_name, output) 


# clase para crear una nueva asignacion
class NewAssignView(View):
    '''
    Clase para crear una asignacion
    '''
    template_name = 'assignations/new_assign.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        Método get
        '''
        query = request.GET.get("q")
        sort = request.GET.get("sort", 'name')
        form = AsignacionForm()
        list_assign = None
        if query:
            list_assign = Asignacion.objects.filter(
                Q(server__name__icontains=query) |
                Q(interface__name_interface__icontains=query) |
                Q(client__name__icontains=query) 
            )
        else:
            list_assign = Asignacion.objects.filter()
        page =request.GET.get("page")
        output = {
            'form': form,
            'list_assign': list_assign
        }
        return render(request, self.template_name, output)

    @method_decorator(login_required)  
    def post(self, request, *args, **kwargs):
        '''
        Método post
        '''
        
        form = AsignacionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/assign/new')    

        output = {
            'form': form,
            'messages': "Revise los campos correctamente.",
        }
        
        return render(request, self.template_name, output) 


# clase para agregar un nuevo cliente
class NewClientView(View):
    '''
    Clase para crear un servidor
    '''
    template_name = 'clients/new_client.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        Método get
        '''
        query = request.GET.get("q")
        sort = request.GET.get("sort", 'name')
        form = ClientForm()
        list_client = None
        if query:
            list_client = Client.objects.filter(
                Q(name__icontains=query) |
                Q(phone__icontains=query) |
                Q(email__icontains=query) 
                
            )
        else:
            list_client = Client.objects.all()
        page =request.GET.get("page")
        output = {
            'form': form,
            'list_client': list_client
        }
        return render(request, self.template_name, output)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        '''
        Método post
        '''
        
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/client/new')    

        output = {
            'form': form,
            'messages': "Revise los campos correctamente.",
        }
        
        return render(request, self.template_name, output) 


# clase para agregar una interfaz
class NewInterfaceView(View):
    '''
    Clase para crear una interfaz
    '''
    template_name = 'interfaces/new_interface.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        Método get
        '''
        query = request.GET.get("q") 
        sort = request.GET.get("sort", 'name')
        form = InterfaceForm()
        list_inter = None
        if query:
            list_inter = Interface.objects.filter(
                Q(name_interface__icontains=query) 
                
            )
        else:
            list_inter = Interface.objects.all()

        output = {
            'form': form,
            'list_inter': list_inter
        }
        return render(request, self.template_name, output)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        '''
        Método post
        '''
        
        form = InterfaceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/interface/new')    

        output = {
            'form': form,
            'messages': "Revise los campos correctamente.",
        }
        
        return render(request, self.template_name, output) 


# clase para agregar una plataforma
class NewPlatformView(View):
    '''
    Clase para agregar una plataforma
    '''
    template_name = 'platforms/new_platform.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        Método get
        '''
        query = request.GET.get("q")
        sort = request.GET.get("sort", 'name')
        form = PlatformForm()
        list_platform = None
        if query:
            list_platform = Platform.objects.filter(
                Q(name_platform__icontains=query) 
               
            )
        else:
            list_platform = Platform.objects.all()
        output = {
            'form': form,
            'list_platform': list_platform
        }
        return render(request, self.template_name, output)

    @method_decorator(login_required)  
    def post(self, request, *args, **kwargs):
        '''
        Método post
        '''
        
        form = PlatformForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/platform/new')    

        output = {
            'form': form,
            'messages': "Revise los campos correctamente.",
        }
        
        return render(request, self.template_name, output) 



# clase para editar un servidor
class ServerEditView(View):
    '''
    Clase para editar los servidores
    '''
    template_name = 'servers/edit_server.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        Método get
        '''
        query = request.GET.get("q")
        sort = request.GET.get("sort", 'name')
        asearch = Server.objects.filter(id=kwargs['id']).first()
        form = ServerEditForm(instance=asearch)
        list_server = None
        if query:
            list_server = Server.objects.filter(
                Q(name__icontains=query)
            )
        else:
            list_server = Server.objects.all()
        
        page =request.GET.get("page")
        output = {
            'form': form,
            'list_server': list_server
        }
        return render(request, self.template_name, output)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        '''
        Método post
        '''
        asearch = Server.objects.filter(id=kwargs['id']).first()
        form = ServerEditForm(request.POST, instance=asearch)
        list_server = Server.objects.all()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')    

        output = {
            'form': form,
            'list_server': list_server,
            'messages': "Revise los campos correctamente.",
        }
        
        return render(request, self.template_name, output)  


# clase para editar una asignacion
class AssignEditView(View):
    '''
    Clase para editar las asignaciones
    '''
    template_name = 'assignations/edit_assign.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        Método get
        '''
        query = request.GET.get("q")
        sort = request.GET.get("sort", 'name')
        asearch = Asignacion.objects.filter(id=kwargs['id']).first()
        form = AsignacionForm(instance=asearch)
        list_assign = None
        if query:
            list_assign = Asignacion.objects.filter(
                Q(server__name__icontains=query) |
                Q(interface__name_interface__icontains=query) |
                Q(client__name__icontains=query) 
            )
        else:
            list_assign = Asignacion.objects.all()
        
        page =request.GET.get("page")
        output = {
            'form': form,
            'list_assign': list_assign
        }
        return render(request, self.template_name, output)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        '''
        Método post
        '''
        asearch = Asignacion.objects.filter(id=kwargs['id']).first()
        form = AsignacionForm(request.POST, instance=asearch)
        list_assign = Asignacion.objects.all()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/assign/new')    

        output = {
            'form': form,
            'list_assign': list_assign,
            'messages': "Revise los campos correctamente.",
        }
        
        return render(request, self.template_name, output)  


# clase para editar un cliente
class ClientEditView(View):
    '''
    Clase para editar los clientes
    '''
    template_name = 'clients/edit_client.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        Método get
        '''
        query = request.GET.get("q")
        sort = request.GET.get("sort", 'name')
        asearch = Client.objects.filter(id=kwargs['id']).first()
        form = ClientForm(instance=asearch)
        list_client = None
        if query:
            list_client = Client.objects.filter(
                Q(name__icontains=query) |
                Q(phone__icontains=query) |
                Q(email__icontains=query) 
            )
        else:
            list_client = Client.objects.all()
        
        page =request.GET.get("page")
        output = {
            'form': form,
            'list_client': list_client
        }
        return render(request, self.template_name, output)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        '''
        Método post
        '''
        asearch = Client.objects.filter(id=kwargs['id']).first()
        form = ClientForm(request.POST, instance=asearch)
        list_client = Client.objects.all()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/client/new')    

        output = {
            'form': form,
            'list_client': list_client,
            'messages': "Revise los campos correctamente.",
        }
        
        return render(request, self.template_name, output) 


# clase para editar una interfaz
class InterfaceEditView(View):
    '''
    Clase para editar las interfaces
    '''
    template_name = 'interfaces/edit_interface.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        Método get
        '''
        query = request.GET.get("q")
        sort = request.GET.get("sort", 'name')
        asearch = Interface.objects.filter(id=kwargs['id']).first()
        form = InterfaceForm(instance=asearch)
        list_inter = None
        if query:
            list_inter = Interface.objects.filter(
                Q(name_interface__icontains=query)      
            )
        else:
            list_inter = Interface.objects.all()
        
        page =request.GET.get("page")
        output = {
            'form': form,
            'list_inter': list_inter
        }
        return render(request, self.template_name, output)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        '''
        Método post
        '''
        asearch = Interface.objects.filter(id=kwargs['id']).first()
        form = InterfaceForm(request.POST, instance=asearch)
        list_inter = Interface.objects.all()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/interface/new')    

        output = {
            'form': form,
            'list_inter': list_inter,
            'messages': "Revise los campos correctamente.",
        }
        
        return render(request, self.template_name, output)  


# clase para editar una plataforma
class PlatformEditView(View):
    '''
    Clase para editar las plataformas
    '''
    template_name = 'platforms/edit_platform.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        Método get
        '''
        query = request.GET.get("q")
        sort = request.GET.get("sort", 'name')
        asearch = Platform.objects.filter(id=kwargs['id']).first()
        form = PlatformForm(instance=asearch)
        list_platform = None
        if query:
            list_platform = Platform.objects.filter(
                Q(name_platform__icontains=query)      
            )
        else:
            list_platform = Platform.objects.all()
        
        page =request.GET.get("page")
        output = {
            'form': form,
            'list_platform': list_platform
        }
        return render(request, self.template_name, output)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        '''
        Método post
        '''
        asearch = Platform.objects.filter(id=kwargs['id']).first()
        form = PlatformForm(request.POST, instance=asearch)
        list_platform = Platform.objects.all()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/platform/new')    

        output = {
            'form': form,
            'list_platform': list_platform,
            'messages': "Revise los campos correctamente.",
        }
        
        return render(request, self.template_name, output) 


class ServerDetailView(View):
    '''
    Clase para ver los detalles del servidor
    '''
    template_name = 'servers/detail_server.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        Método get
        '''
        query = request.GET.get("q")
        sort = request.GET.get("sort", 'name')
        asearch = Asignacion.objects.filter(server=kwargs['id']).first()
        form = AsignacionForm(instance=asearch)
        list_asignacion = Asignacion.objects.filter(server=kwargs['id'])
        list_server = Server.objects.filter(id=kwargs['id'])
        list_client = AsignacionCliente.objects.filter(server=kwargs['id'])
        list_platform = Platform.objects.filter(id=kwargs['id'])

        page =request.GET.get("page")
        output = {
            'form': form,
            'list_asignacion': list_asignacion,
            'list_server': list_server,
            'list_client': list_client,
            'list_platform': list_platform
        }
        return render(request, self.template_name, output)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        '''
        Método post
        '''
        asearch = Asignacion.objects.filter(id=kwargs['id']).first()
        form = AsignacionForm(request.POST, instance=asearch)
        list_server = Asignacion.objects.all()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/server/detail')    

        output = {
            'form': form,
            'list_server': list_server,
            'messages': "Revise los campos correctamente.",
        }
        
        return render(request, self.template_name, output) 


# clase para crear una nueva asignacion de los clientes
class NewAssignClientView(View):
    '''
    Clase para crear una asignacion de los clientes
    '''
    template_name = 'assignations_client/new_assign.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        Método get
        '''
        query = request.GET.get("q")
        sort = request.GET.get("sort", 'name')
        form = AsignacionClienteForm()
        list_assignC = None
        if query:
            list_assignC = AsignacionCliente.objects.filter(
                Q(server__name__icontains=query) |
                Q(client__name__icontains=query) 
            )
        else:
            list_assignC = AsignacionCliente.objects.all()
        page =request.GET.get("page")
        output = {
            'form': form,
            'list_assignC': list_assignC
        }
        return render(request, self.template_name, output)

    @method_decorator(login_required)  
    def post(self, request, *args, **kwargs):
        '''
        Método post
        '''
        
        form = AsignacionClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/assignClient/new')    

        output = {
            'form': form,
            'messages': "Revise los campos correctamente.",
        }
        
        return render(request, self.template_name, output) 



# clase para editar una asignacion de los clientes
class AssignClientEditView(View):
    '''
    Clase para editar las asignaciones de los clientes
    '''
    template_name = 'assignations_client/edit_assign.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        Método get
        '''
        query = request.GET.get("q")
        sort = request.GET.get("sort", 'name')
        asearch = AsignacionCliente.objects.filter(id=kwargs['id']).first()
        form = AsignacionClienteForm(instance=asearch)
        list_assignC = None
        if query:
            list_assignC = AsignacionCliente.objects.filter(
                Q(server__name__icontains=query) |
                Q(client__name__icontains=query) 
            )
        else:
            list_assignC = AsignacionCliente.objects.all()
        
        page =request.GET.get("page")
        output = {
            'form': form,
            'list_assignC': list_assignC
        }
        return render(request, self.template_name, output)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        '''
        Método post
        '''
        asearch = AsignacionCliente.objects.filter(id=kwargs['id']).first()
        form = AsignacionClienteForm(request.POST, instance=asearch)
        list_assignC = AsignacionCliente.objects.all()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/assignClient/new')    

        output = {
            'form': form,
            'list_assignC': list_assignC,
            'messages': "Revise los campos correctamente.",
        }
        
        return render(request, self.template_name, output) 





