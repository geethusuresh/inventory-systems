# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ReportTest'
        db.create_table(u'reports_reporttest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file_name', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'reports', ['ReportTest'])

    def backwards(self, orm):
        # Deleting model 'ReportTest'
        db.delete_table(u'reports_reporttest')

    models = {
        u'reports.reporttest': {
            'Meta': {'object_name': 'ReportTest'},
            'file_name': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['reports']