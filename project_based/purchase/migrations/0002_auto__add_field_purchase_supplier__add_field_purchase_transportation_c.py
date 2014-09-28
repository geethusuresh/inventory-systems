# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Purchase.supplier'
        db.add_column(u'purchase_purchase', 'supplier',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Supplier'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Purchase.transportation_company'
        db.add_column(u'purchase_purchase', 'transportation_company',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.TransportationCompany'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'SupplierAccount.supplier'
        db.add_column(u'purchase_supplieraccount', 'supplier',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['web.Supplier'], unique=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Purchase.supplier'
        db.delete_column(u'purchase_purchase', 'supplier_id')

        # Deleting field 'Purchase.transportation_company'
        db.delete_column(u'purchase_purchase', 'transportation_company_id')

        # Deleting field 'SupplierAccount.supplier'
        db.delete_column(u'purchase_supplieraccount', 'supplier_id')

    models = {
        u'project.item': {
            'Meta': {'object_name': 'Item'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_type': ('django.db.models.fields.CharField', [], {'default': "'item'", 'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'project.project': {
            'Meta': {'object_name': 'Project'},
            'budget_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'expected_end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'expense_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'purchase_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'sales_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'purchase.purchase': {
            'Meta': {'object_name': 'Purchase'},
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'cheque_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cheque_no': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'discount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'discount_percentage': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'grant_total': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_paid_completely': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'net_total': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'payment_mode': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['project.Project']", 'null': 'True', 'blank': 'True'}),
            'purchase_expense': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'purchase_invoice_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'purchase_invoice_number': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Supplier']", 'null': 'True', 'blank': 'True'}),
            'supplier_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'supplier_do_number': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '10'}),
            'supplier_invoice_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'supplier_invoice_number': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '10'}),
            'transportation_company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.TransportationCompany']", 'null': 'True', 'blank': 'True'})
        },
        u'purchase.purchaseitem': {
            'Meta': {'object_name': 'PurchaseItem'},
            'cost_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['project.Item']", 'null': 'True', 'blank': 'True'}),
            'net_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '3'}),
            'purchase': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['purchase.Purchase']", 'null': 'True', 'blank': 'True'}),
            'quantity_purchased': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'purchase.supplieraccount': {
            'Meta': {'object_name': 'SupplierAccount'},
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '3'}),
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'branch_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'cheque_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cheque_no': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'narration': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'paid_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '3'}),
            'payment_mode': ('django.db.models.fields.CharField', [], {'default': "'cash'", 'max_length': '10'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Supplier']", 'unique': 'True'}),
            'total_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '3'})
        },
        u'web.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'contact_person': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'email_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'house_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'land_line': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'pin': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        u'web.transportationcompany': {
            'Meta': {'object_name': 'TransportationCompany'},
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['purchase']