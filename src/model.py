import json
from datetime import datetime
from django.db import models
from django.forms.models import model_to_dict
from django.core import serializers
from .middleware import current_request
from library.utilities import json_serial 
from src.manager import CustomManager
from django.contrib.auth.models import User

class ActivityLog(models.Model):
    '''
    Contiene los campos base de los demas modelos.
    '''
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name='Creado por', related_name='%(app_label)s_%(class)s_created_by')
    action = models.CharField('Acción', max_length=100)
    old_values = models.TextField('Valores anteriores')
    new_values = models.TextField('Valores nuevos')
    class Meta:
        app_label='application'
        
class BaseModel(models.Model):
    '''
    Contiene los campos base de los demas modelos.
    '''

    created_at = models.DateTimeField('Fecha de creación')
    updated_at = models.DateTimeField('Fecha última de modificación', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Creado por', related_name='%(app_label)s_%(class)s_created_by')
    updated_by = models.ForeignKey(User, verbose_name='Última modificación por', related_name='%(app_label)s_%(class)s_updated_by', null=True, blank=True)
    is_active = models.BooleanField('Estado', default=True)
    deleted = models.BooleanField('Eliminado', default=False)
    
    objects = CustomManager()
    
    def delete(self):
        '''
        Sobreescribir el método eliminar, para no eliminar físicamente de la
        base de datos, solo hacer un update.
        '''
        self.deleted = True
        self.save()
    
    def save(self, *args, **kwargs):
        '''
        Sobreescribir el metodo save para colocar de forma automatica el usuario creador o el quien actualiza.
        '''
        request = current_request()
        log = ActivityLog()
        log.created_by = request.current_request.user
        if self._state.adding:
            self.created_by = request.current_request.user
            self.created_at = datetime.now().date()
            super().save(*args, **kwargs)
            log.action = 'Registro ' + self._meta.verbose_name.title()
            instance = self.to_dict()
            instance = { self._meta.get_field(key).verbose_name: value for key, value in instance.items() }
            log.new_values = json.dumps(instance, default=json_serial)
        else:
            self.updated_by = request.current_request.user
            self.updated_at = datetime.now().date()
            super().save(*args, **kwargs)
            log.action = 'Actualización ' + self._meta.verbose_name.title()
            new_values= self.to_dict()
            old_values = json.loads(self.old_values)
            old_values_save = {}
            old_values_save = {self._meta.get_field(old).verbose_name: old_values[old] for old in old_values }      
            changed = { self._meta.get_field(key).verbose_name: value for key, value in new_values.items() if value != old_values[key] }
            log.new_values = json.dumps(changed, default=json_serial)
            log.old_values =  json.dumps(old_values_save, default=json_serial)
        log.save()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_values = json.dumps(self.to_dict(), default=json_serial)

    def to_dict(self):
        output = model_to_dict(self)
        if 'created_by' in output and output['created_by'] is not None:
            output['created_by'] = self.created_by.username
        if 'updated_by' in output and output['updated_by'] is not None:
            output['updated_by'] = self.updated_by.username
        output['is_active'] = 'activo' if self.is_active else 'inactivo'
        output['deleted'] = 'eliminado' if self.is_active else 'no eliminado'
        return output
    class Meta:
        abstract = True
