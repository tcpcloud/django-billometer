# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ResourceTypeData'
        db.delete_table('billometer_resourcetypedata')

        # Deleting field 'ResourceInstanceData.start'
        db.delete_column('billometer_resourceinstancedata', 'start')

        # Deleting field 'ResourceInstanceData.end'
        db.delete_column('billometer_resourceinstancedata', 'end')

        # Adding field 'ResourceInstanceData.date'
        db.add_column('billometer_resourceinstancedata', 'date',
                      self.gf('django.db.models.fields.DateField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'ResourceInstanceData.closed'
        db.add_column('billometer_resourceinstancedata', 'closed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'ResourceTypeData'
        db.create_table('billometer_resourcetypedata', (
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billometer.ResourceType'])),
            ('value', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=18, decimal_places=3)),
            ('start', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('billometer', ['ResourceTypeData'])

        # Adding field 'ResourceInstanceData.start'
        db.add_column('billometer_resourceinstancedata', 'start',
                      self.gf('django.db.models.fields.DateField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'ResourceInstanceData.end'
        db.add_column('billometer_resourceinstancedata', 'end',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'ResourceInstanceData.date'
        db.delete_column('billometer_resourceinstancedata', 'date')

        # Deleting field 'ResourceInstanceData.closed'
        db.delete_column('billometer_resourceinstancedata', 'closed')


    models = {
        'billometer.project': {
            'Meta': {'object_name': 'Project'},
            'customer_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'customer_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'extra': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'openstack_tenant': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'billometer.resourceinstance': {
            'Meta': {'object_name': 'ResourceInstance'},
            'ceilometer_query': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extra': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'openstack_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resource_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billometer.ResourceType']"})
        },
        'billometer.resourceinstancedata': {
            'Meta': {'object_name': 'ResourceInstanceData'},
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '18', 'decimal_places': '6'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billometer.ResourceInstance']"}),
            'value': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '18', 'decimal_places': '3'})
        },
        'billometer.resourcetype': {
            'Meta': {'object_name': 'ResourceType'},
            'ceilometer_query': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'default_price': ('django.db.models.fields.DecimalField', [], {'default': "'1'", 'max_digits': '18', 'decimal_places': '6'}),
            'default_threshold': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '18', 'decimal_places': '3'}),
            'extra': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'openstack_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billometer.Project']"}),
            'resource': ('django.db.models.fields.CharField', [], {'default': "'nova.instance'", 'max_length': '255'})
        }
    }

    complete_apps = ['billometer']