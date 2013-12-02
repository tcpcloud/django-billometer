# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'BillingRate'
        db.delete_table('billometer_billingrate')

        # Adding field 'Project.extra'
        db.add_column('billometer_project', 'extra',
                      self.gf('django.db.models.fields.TextField')(default='{}', null=True, blank=True),
                      keep_default=False)

        # Adding field 'ResourceInstanceData.price'
        db.add_column('billometer_resourceinstancedata', 'price',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=18, decimal_places=6),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'BillingRate'
        db.create_table('billometer_billingrate', (
            ('instance_hdd_limit', self.gf('django.db.models.fields.BigIntegerField')(default=1000000)),
            ('instance_net_io', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=3)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('volume_10k', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=3)),
            ('instance_large', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=3)),
            ('instance_hdd_io', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=3)),
            ('instance_net_limit', self.gf('django.db.models.fields.BigIntegerField')(default=1000000)),
            ('volume_snapshots', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('kind', self.gf('django.db.models.fields.CharField')(default='tenant', max_length=55)),
            ('instance_medium', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=3)),
            ('instance_small', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=3)),
            ('volume_easy', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=3)),
            ('volume_7k', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=3)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')()),
            ('volume_io', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=3)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('billometer', ['BillingRate'])

        # Deleting field 'Project.extra'
        db.delete_column('billometer_project', 'extra')

        # Deleting field 'ResourceInstanceData.price'
        db.delete_column('billometer_resourceinstancedata', 'price')


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
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '18', 'decimal_places': '6'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billometer.ResourceInstance']"}),
            'start': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '18', 'decimal_places': '3'})
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