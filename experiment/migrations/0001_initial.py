# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Experiment'
        db.create_table('experiment_experiment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('period', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('experiment', ['Experiment'])

        # Adding M2M table for field user on 'Experiment'
        db.create_table('experiment_experiment_user', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('experiment', models.ForeignKey(orm['experiment.experiment'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('experiment_experiment_user', ['experiment_id', 'user_id'])

        # Adding M2M table for field dev on 'Experiment'
        db.create_table('experiment_experiment_dev', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('experiment', models.ForeignKey(orm['experiment.experiment'], null=False)),
            ('device', models.ForeignKey(orm['device.device'], null=False))
        ))
        db.create_unique('experiment_experiment_dev', ['experiment_id', 'device_id'])

        # Adding M2M table for field app on 'Experiment'
        db.create_table('experiment_experiment_app', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('experiment', models.ForeignKey(orm['experiment.experiment'], null=False)),
            ('application', models.ForeignKey(orm['application.application'], null=False))
        ))
        db.create_unique('experiment_experiment_app', ['experiment_id', 'application_id'])

        # Adding model 'ExperimentProfile'
        db.create_table('experiment_experimentprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experiment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['experiment.Experiment'])),
            ('starttime', self.gf('django.db.models.fields.DateTimeField')()),
            ('endtime', self.gf('django.db.models.fields.DateTimeField')()),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('experiment', ['ExperimentProfile'])

    def backwards(self, orm):
        # Deleting model 'Experiment'
        db.delete_table('experiment_experiment')

        # Removing M2M table for field user on 'Experiment'
        db.delete_table('experiment_experiment_user')

        # Removing M2M table for field dev on 'Experiment'
        db.delete_table('experiment_experiment_dev')

        # Removing M2M table for field app on 'Experiment'
        db.delete_table('experiment_experiment_app')

        # Deleting model 'ExperimentProfile'
        db.delete_table('experiment_experimentprofile')

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
        'experiment.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'app': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['application.Application']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'dev': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['device.Device']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'period': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'})
        },
        'experiment.experimentprofile': {
            'Meta': {'object_name': 'ExperimentProfile'},
            'endtime': ('django.db.models.fields.DateTimeField', [], {}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiment.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'starttime': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['experiment']