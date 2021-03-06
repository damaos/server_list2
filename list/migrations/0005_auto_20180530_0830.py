# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-30 13:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0004_auto_20180524_1323'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsignacionCliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='list.Client', verbose_name=b'Cliente')),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='list.Server', verbose_name=b'Servidor')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'Asignacion de Cliente',
                'verbose_name_plural': 'Asignacion de Clientes',
            },
        ),
        migrations.AddField(
            model_name='interface',
            name='ip',
            field=models.CharField(default=1, max_length=250, unique=True, verbose_name=b'IP'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='interface',
            name='port',
            field=models.CharField(default=0, max_length=255, verbose_name=b'Puerto'),
            preserve_default=False,
        ),
    ]
