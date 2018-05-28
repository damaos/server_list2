# -*- coding: utf-8 -*-
from django.db import models

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
    client = models.ForeignKey(Client, verbose_name= 'Cliente', on_delete=models.CASCADE,)

    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Asignaciones'
        verbose_name = 'Asignacion'