# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Device'
        db.create_table('device_device', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meid', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('reg_id', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('collapse_key', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('last_messaged', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('failed_push', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('update_interval', self.gf('django.db.models.fields.CharField')(default=10, max_length=5)),
            ('active', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('device', ['Device'])

        # Adding model 'DeviceApplication'
        db.create_table('device_deviceapplication', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dev', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['device.Device'])),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['application.Application'])),
        ))
        db.send_create_signal('device', ['DeviceApplication'])

        # Adding unique constraint on 'DeviceApplication', fields ['dev', 'app']
        db.create_unique('device_deviceapplication', ['dev_id', 'app_id'])

        # Adding model 'DeviceProfile'
        db.create_table('device_deviceprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dev', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['device.Device'], unique=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('last_log', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('phone_no', self.gf('django.db.models.fields.CharField')(max_length=13, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('plan', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('image_version', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('service_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('install_permission', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('device', ['DeviceProfile'])


    def backwards(self, orm):
        # Removing unique constraint on 'DeviceApplication', fields ['dev', 'app']
        db.delete_unique('device_deviceapplication', ['dev_id', 'app_id'])

        # Deleting model 'Device'
        db.delete_table('device_device')

        # Deleting model 'DeviceApplication'
        db.delete_table('device_deviceapplication')

        # Deleting model 'DeviceProfile'
        db.delete_table('device_deviceprofile')


    models = {
        'application.application': {
            'Meta': {'object_name': 'Application'},
            'active': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'endtime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'starttime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'device.device': {
            'Meta': {'object_name': 'Device'},
            'active': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'collapse_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'failed_push': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_messaged': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'meid': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'reg_id': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'update_interval': ('django.db.models.fields.CharField', [], {'default': '10', 'max_length': '5'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'device.deviceapplication': {
            'Meta': {'unique_together': "(('dev', 'app'),)", 'object_name': 'DeviceApplication'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['application.Application']"}),
            'dev': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['device.Device']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'device.deviceprofile': {
            'Meta': {'object_name': 'DeviceProfile'},
            'dev': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['device.Device']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_version': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'install_permission': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_log': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True', 'blank': 'True'}),
            'plan': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'service_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['device']