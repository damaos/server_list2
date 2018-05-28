# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-24 16:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asignacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'Asignacion',
                'verbose_name_plural': 'Asignaciones',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name=b'Nombre')),
                ('phone', models.IntegerField(unique=True, verbose_name=b'Telefono')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name=b'Correo')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_interface', models.CharField(max_length=255, unique=True, verbose_name=b'Nombre interfaz')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'Interfaz',
                'verbose_name_plural': 'Interfaces',
            },
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_platform', models.CharField(max_length=255, verbose_name=b'Nombre de Plataforma')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'Plataforma',
                'verbose_name_plural': 'Plataformas',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name=b'Nombre')),
                ('tipe', models.CharField(max_length=255, verbose_name=b'Tipo')),
                ('num_interface', models.IntegerField(default=0, verbose_name=b'Numero de interfaces')),
                ('virtual', models.CharField(choices=[(b'SI', b'SI'), (b'NO', b'NO')], max_length=3, verbose_name=b'Virtualizacion')),
                ('system_operative', models.CharField(max_length=255, verbose_name=b'Sistema')),
                ('model', models.CharField(max_length=255, verbose_name=b'Modelo')),
                ('service', models.CharField(max_length=255, verbose_name=b'Servicio')),
                ('city', models.CharField(max_length=255, verbose_name=b'Ciudad')),
                ('seat', models.CharField(max_length=255, verbose_name=b'Sede')),
                ('rack', models.CharField(max_length=255, verbose_name=b'Rack')),
                ('observation', models.TextField(verbose_name=b'Observacion')),
                ('is_active', models.BooleanField(default=True, verbose_name=b'Estado')),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='list.Platform', verbose_name=b'Plataforma')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'Servidor',
                'verbose_name_plural': 'Servidores',
            },
        ),
        migrations.AddField(
            model_name='asignacion',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='list.Client', verbose_name=b'Cliente'),
        ),
        migrations.AddField(
            model_name='asignacion',
            name='interface',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='list.Interface', verbose_name=b'Interfaz'),
        ),
        migrations.AddField(
            model_name='asignacion',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='list.Server', verbose_name=b'Servidor'),
        ),
    ]
