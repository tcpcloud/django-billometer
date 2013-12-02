# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name', blank=True)),
                ('openstack_tenant', models.CharField(max_length=255, null=True, verbose_name='openstack tenant uid', blank=True)),
                ('customer_name', models.CharField(max_length=255, null=True, verbose_name='customer name', blank=True)),
                ('customer_id', models.CharField(max_length=255, null=True, verbose_name='customer id', blank=True)),
                ('extra', django_extensions.db.fields.json.JSONField(null=True, verbose_name='extra', blank=True)),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='ResourceInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name', blank=True)),
                ('openstack_id', models.CharField(max_length=255, null=True, verbose_name='openstack id', blank=True)),
                ('ceilometer_query', models.TextField(null=True, verbose_name='ceilometer query', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='is active ?')),
                ('extra', django_extensions.db.fields.json.JSONField(null=True, verbose_name='extra', blank=True)),
            ],
            options={
                'verbose_name': 'resource instance',
                'verbose_name_plural': 'resource instances',
            },
        ),
        migrations.CreateModel(
            name='ResourceInstanceData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(null=True, blank=True)),
                ('closed', models.BooleanField(default=False)),
                ('value', models.DecimalField(default=0, verbose_name='value', max_digits=18, decimal_places=3)),
                ('price', models.DecimalField(default=0, verbose_name='price', max_digits=18, decimal_places=6)),
                ('resource', models.ForeignKey(to='billometer.ResourceInstance')),
            ],
            options={
                'verbose_name': 'resource instance data',
                'verbose_name_plural': 'resource instance data',
            },
        ),
        migrations.CreateModel(
            name='ResourceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name', blank=True)),
                ('resource', models.CharField(default=b'nova.instance', max_length=255, verbose_name='type', choices=[(b'nova.cpu', 'Nova CPU'), (b'nova.memory', 'Nova memory'), (b'nova.instance', 'Nova instance'), (b'cinder.volume', 'Cinder volume'), (b'glance.image', 'Glance image'), (b'glance.snapshot', 'Glance snapshot'), (b'neutron.floating_ip', 'Neutron floating IP'), (b'neutron.network', 'Neutron network'), (b'neutron.router', 'Neutron router')])),
                ('openstack_id', models.CharField(max_length=255, null=True, verbose_name='openstack id', blank=True)),
                ('ceilometer_query', models.TextField(verbose_name='id', null=True, editable=False, blank=True)),
                ('default_price', models.DecimalField(default=b'1', verbose_name='price', max_digits=18, decimal_places=6)),
                ('default_threshold', models.DecimalField(default=b'0', verbose_name='threshold', max_digits=18, decimal_places=3)),
                ('extra', django_extensions.db.fields.json.JSONField(null=True, verbose_name='extra', blank=True)),
                ('project', models.ForeignKey(verbose_name='project', to='billometer.Project')),
            ],
            options={
                'verbose_name': 'resource type',
                'verbose_name_plural': 'resource types',
            },
        ),
        migrations.AddField(
            model_name='resourceinstance',
            name='resource_type',
            field=models.ForeignKey(verbose_name='resource type', to='billometer.ResourceType'),
        ),
    ]
