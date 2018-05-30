from django.contrib import admin

from .models import Server, Client, Interface, Asignacion, Platform, AsignacionCliente


@admin.register(Server)
class AdminServer(admin.ModelAdmin):
    list_display = ('name','tipe', 'num_interface', 'virtual', 'platform', 'system_operative', 'model', 'service', 'city', 'seat', 'rack', 'observation', )
    list_filter = ('name','tipe', 'num_interface', 'virtual', 'platform', 'system_operative', 'model', 'service', 'city', 'seat', 'rack', 'observation', )

@admin.register(Client)
class AdminClient(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email',)
    list_filter = ('name',)

@admin.register(Interface)
class AdminInterface(admin.ModelAdmin):
    list_display = ('name_interface','ip', 'port',)
    list_filter = ('name_interface',)

@admin.register(Asignacion)
class AdminAsignacion(admin.ModelAdmin):
    list_display = ('server', 'interface',)
    list_filter = ('server', )

@admin.register(Platform)
class AdminPlatform(admin.ModelAdmin):
    list_display = ('name_platform',)
    list_filter = ('name_platform',)


@admin.register(AsignacionCliente)
class AdminAsignacionCliente(admin.ModelAdmin):
    list_display = ('server', 'client',)
    list_filter = ('server',)