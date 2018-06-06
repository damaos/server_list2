# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


choice_option = ('SI', 'SI',),('NO', 'NO',)

# Clientes
class Client(models.Model):
    name = models.CharField('Nombre', max_length=255)
    phone = models.IntegerField('Telefono', unique=True)
    email = models.EmailField('Correo', max_length=255, unique=True)
    is_active = models.BooleanField('Estado', default=True)

    
    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Clientes'
    	# verbose_name = 'Cliente'


#  Interfaz
class Interface(models.Model):
    name_interface = models.CharField('Nombre interfaz', max_length=255, unique=True)
    ip =  models.CharField('IP', max_length=250, unique=True)
    port = models.CharField('Puerto', max_length=255,)
    is_asignada = models.BooleanField('Estado de Asignacion', default=False)

    def __str__(self):
        return '%s' % self.name_interface
    
    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Interfaces'
        verbose_name = 'Interfaz'

# Plataforma
class Platform(models.Model):
    name_platform = models.CharField('Nombre de Plataforma', max_length=255,)
    is_active = models.BooleanField('Estado', default=True)


    def __str__(self):
        return '%s' % self.name_platform
    
    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Plataformas'
        verbose_name = 'Plataforma'
        

# Servidor
class Server(models.Model):
    name = models.CharField('Nombre', max_length=255, unique=True,)
    tipe = models.CharField('Tipo', max_length=255)
    num_interface = models.IntegerField('Numero de interfaces', default=0)
    virtual = models.BooleanField('Virtualizacion', default=False )  
    platform = models.ForeignKey(Platform, verbose_name='Plataforma', on_delete=models.CASCADE)
    system_operative = models.CharField('Sistema', max_length=255)
    model = models.CharField('Modelo', max_length=255)
    service = models.CharField('Servicio', max_length=255)
    city = models.CharField('Ciudad', max_length=255)
    seat = models.CharField('Sede', max_length=255)
    rack = models.CharField('Rack', max_length=255)
    observation = models.TextField('Observacion')
    is_active = models.BooleanField('Estado', default=True)

    def __str__(self):
        return '%s' % self.name
    
    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Servidores'
        verbose_name = 'Servidor'

class Asignacion(models.Model):
    server = models.ForeignKey(Server, verbose_name= 'Servidor', on_delete=models.CASCADE)
    interface = models.ForeignKey(Interface, verbose_name = 'Interfaz', on_delete=models.CASCADE,)

    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Asignaciones'
        verbose_name = 'Asignacion'


class AsignacionCliente(models.Model):
    server = models.ForeignKey(Server, verbose_name= 'Servidor', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, verbose_name= 'Cliente', on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Asignacion de Clientes'
        verbose_name = 'Asignacion de Cliente'




class Maestra(models.Model):
    server  = models.ForeignKey(Server, verbose_name= 'Servidor', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, verbose_name= 'Cliente', on_delete=models.CASCADE)
    asignacion = models.ForeignKey(Asignacion, verbose_name= 'Asignacion', on_delete=models.CASCADE)
    asignacionclient = models.ForeignKey(AsignacionCliente, verbose_name= 'Asignacion Cliente', on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, verbose_name= 'Plataforma', on_delete=models.CASCADE)
    interface = models.ForeignKey(Interface, verbose_name= 'Interface', on_delete=models.CASCADE)
