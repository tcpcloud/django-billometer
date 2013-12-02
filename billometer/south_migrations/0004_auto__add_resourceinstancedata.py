# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ResourceInstanceData'
        db.create_table('billometer_resourceinstancedata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billometer.ResourceInstance'])),
            ('start', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('value', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=18, decimal_places=3)),
        ))
        db.send_create_signal('billometer', ['ResourceInstanceData'])


    def backwards(self, orm):
        # Deleting model 'ResourceInstanceData'
        db.delete_table('billometer_resourceinstancedata')


    models = {
        'billometer.billingrate': {
            'Meta': {'object_name': 'BillingRate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance_hdd_io': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
            'instance_hdd_limit': ('django.db.models.fields.BigIntegerField', [], {'default': '1000000'}),
            'instance_large': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
            'instance_medium': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
            'instance_net_io': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
            'instance_net_limit': ('django.db.models.fields.BigIntegerField', [], {'default': '1000000'}),
            'instance_small': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
            'kind': ('django.db.models.fields.CharField', [], {'default': "'tenant'", 'max_length': '55'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'volume_10k': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
            'volume_7k': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
            'volume_easy': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
            'volume_io': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
            'volume_snapshots': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'billometer.project': {
            'Meta': {'object_name': 'Project'},
            'customer_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'customer_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'openstack_tenant': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'billometer.resourceinstance': {
            'Meta': {'object_name': 'ResourceInstance'},
            'ceilometer_query': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'openstack_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resource_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billometer.ResourceType']"})
        },
        'billometer.resourceinstancedata': {
            'Meta': {'object_name': 'ResourceInstanceData'},
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billometer.ResourceInstance']"}),
            'start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '18', 'decimal_places': '3'})
        },
        'billometer.resourcetype': {
            'Meta': {'object_name': 'ResourceType'},
            'ceilometer_query': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'default_price': ('django.db.models.fields.DecimalField', [], {'default': "'1'", 'max_digits': '18', 'decimal_places': '3'}),
            'default_threshold': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '18', 'decimal_places': '3'}),
            'flavor': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billometer.Project']"}),
            'resource': ('django.db.models.fields.CharField', [], {'default': "'nova.instance'", 'max_length': '255'})
        },
        'billometer.resourcetypedata': {
            'Meta': {'object_name': 'ResourceTypeData'},
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billometer.ResourceType']"}),
            'start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '18', 'decimal_places': '3'})
        }
    }

    complete_apps = ['billometer']