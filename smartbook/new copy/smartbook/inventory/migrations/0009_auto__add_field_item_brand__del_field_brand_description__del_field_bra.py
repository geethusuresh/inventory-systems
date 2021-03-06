# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Item.brand'
        db.add_column(u'inventory_item', 'brand',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['inventory.Brand']),
                      keep_default=False)

        # Deleting field 'Brand.description'
        db.delete_column(u'inventory_brand', 'description')

        # Deleting field 'Brand.name'
        db.delete_column(u'inventory_brand', 'name')

        # Adding field 'Brand.brand'
        db.add_column(u'inventory_brand', 'brand',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=50),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Item.brand'
        db.delete_column(u'inventory_item', 'brand_id')


        # User chose to not deal with backwards NULL issues for 'Brand.description'
        raise RuntimeError("Cannot reverse this migration. 'Brand.description' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Brand.name'
        raise RuntimeError("Cannot reverse this migration. 'Brand.name' and its values cannot be restored.")
        # Deleting field 'Brand.brand'
        db.delete_column(u'inventory_brand', 'brand')

    models = {
        u'inventory.brand': {
            'Meta': {'object_name': 'Brand'},
            'brand': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'inventory.inventory': {
            'Meta': {'object_name': 'Inventory'},
            'discount_permit': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'selling_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'unit_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'})
        },
        u'inventory.item': {
            'Meta': {'object_name': 'Item'},
            'barcode': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Brand']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tax': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'})
        },
        u'inventory.unitofmeasure': {
            'Meta': {'object_name': 'UnitOfMeasure'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uom': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['inventory']
