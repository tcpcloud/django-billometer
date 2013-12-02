# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BillingRate'
        db.create_table(u'billometer_billingrate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('kind', self.gf('django.db.models.fields.CharField')(default='tenant', max_length=55)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('instance_small', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=3)),
            ('instance_medium', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=3)),
            ('instance_large', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=3)),
            ('instance_hdd_io', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=3)),
            ('instance_hdd_limit', self.gf('django.db.models.fields.BigIntegerField')(default=1000000)),
            ('instance_net_io', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=3)),
            ('instance_net_limit', self.gf('django.db.models.fields.BigIntegerField')(default=1000000)),
            ('volume_easy', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=3)),
            ('volume_10k', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=3)),
            ('volume_7k', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=3)),
            ('volume_io', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=3)),
            ('volume_snapshots', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'billometer', ['BillingRate'])

        # Adding model 'Project'
        db.create_table(u'billometer_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('openstack_tenant', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'billometer', ['Project'])

        # Adding model 'ResourceTypeData'
        db.create_table(u'billometer_resourcetypedata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billometer.ResourceType'])),
            ('start', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('value', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=18, decimal_places=3)),
        ))
        db.send_create_signal(u'billometer', ['ResourceTypeData'])

        # Adding model 'ResourceType'
        db.create_table(u'billometer_resourcetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billometer.Project'])),
            ('resource', self.gf('django.db.models.fields.CharField')(default='nova.instance', max_length=255)),
            ('ceilometer_query', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('default_price', self.gf('django.db.models.fields.DecimalField')(default='1', max_digits=18, decimal_places=3)),
            ('default_threshold', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=18, decimal_places=3)),
        ))
        db.send_create_signal(u'billometer', ['ResourceType'])

        # Adding model 'ResourceInstance'
        db.create_table(u'billometer_resourceinstance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('openstack_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('ceilometer_query', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('resource_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billometer.ResourceType'])),
        ))
        db.send_create_signal(u'billometer', ['ResourceInstance'])


    def backwards(self, orm):
        # Deleting model 'BillingRate'
        db.delete_table(u'billometer_billingrate')

        # Deleting model 'Project'
        db.delete_table(u'billometer_project')

        # Deleting model 'ResourceTypeData'
        db.delete_table(u'billometer_resourcetypedata')

        # Deleting model 'ResourceType'
        db.delete_table(u'billometer_resourcetype')

        # Deleting model 'ResourceInstance'
        db.delete_table(u'billometer_resourceinstance')


    models = {
        u'billometer.billingrate': {
            'Meta': {'object_name': 'BillingRate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        u'billometer.project': {
            'Meta': {'object_name': 'Project'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'openstack_tenant': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'billometer.resourceinstance': {
            'Meta': {'object_name': 'ResourceInstance'},
            'ceilometer_query': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'openstack_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resource_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['billometer.ResourceType']"})
        },
        u'billometer.resourcetype': {
            'Meta': {'object_name': 'ResourceType'},
            'ceilometer_query': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'default_price': ('django.db.models.fields.DecimalField', [], {'default': "'1'", 'max_digits': '18', 'decimal_places': '3'}),
            'default_threshold': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '18', 'decimal_places': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['billometer.Project']"}),
            'resource': ('django.db.models.fields.CharField', [], {'default': "'nova.instance'", 'max_length': '255'})
        },
        u'billometer.resourcetypedata': {
            'Meta': {'object_name': 'ResourceTypeData'},
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['billometer.ResourceType']"}),
            'start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '18', 'decimal_places': '3'})
        }
    }

    complete_apps = ['billometer']