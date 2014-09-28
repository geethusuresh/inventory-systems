# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Purchase'
        db.create_table(u'purchase_purchase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project.Project'], null=True, blank=True)),
            ('purchase_invoice_number', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('supplier_invoice_number', self.gf('django.db.models.fields.CharField')(default='1', max_length=10)),
            ('supplier_do_number', self.gf('django.db.models.fields.CharField')(default='1', max_length=10)),
            ('supplier_invoice_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('purchase_invoice_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('payment_mode', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('bank_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('cheque_no', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('cheque_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('discount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('discount_percentage', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('net_total', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('supplier_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('grant_total', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('purchase_expense', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('is_paid_completely', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'purchase', ['Purchase'])

        # Adding model 'PurchaseItem'
        db.create_table(u'purchase_purchaseitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project.Item'], null=True, blank=True)),
            ('purchase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['purchase.Purchase'], null=True, blank=True)),
            ('quantity_purchased', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('cost_price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=3)),
            ('net_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=3)),
        ))
        db.send_create_signal(u'purchase', ['PurchaseItem'])

        # Adding model 'SupplierAccount'
        db.create_table(u'purchase_supplieraccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('payment_mode', self.gf('django.db.models.fields.CharField')(default='cash', max_length=10)),
            ('narration', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('total_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=3)),
            ('paid_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=3)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=3)),
            ('cheque_no', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cheque_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('bank_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('branch_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'purchase', ['SupplierAccount'])

    def backwards(self, orm):
        # Deleting model 'Purchase'
        db.delete_table(u'purchase_purchase')

        # Deleting model 'PurchaseItem'
        db.delete_table(u'purchase_purchaseitem')

        # Deleting model 'SupplierAccount'
        db.delete_table(u'purchase_supplieraccount')

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
            'supplier_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'supplier_do_number': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '10'}),
            'supplier_invoice_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'supplier_invoice_number': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '10'})
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
            'total_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '3'})
        }
    }

    complete_apps = ['purchase']