from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

from project.models import Project, ProjectItem, Item, InventoryItem
from web.models import Customer, CashInHand, CashEntry


PAYMENT_MODE = (
    ('cash', 'Cash'),
    ('cheque', 'Cheque'),
    ('credit', 'Credit'),
)

class DeliveryNote(models.Model):
    project = models.ForeignKey(Project, null=True, blank=True)
    customer = models.ForeignKey(Customer, null=True, blank=True)
    delivery_note_number = models.CharField('Delivery Note Serial number', max_length=50, null=True, blank=True, unique=True)
    date = models.DateField('Date', null=True, blank=True)
    lpo_number = models.CharField('LPO Number', null=True, blank=True, max_length=20)
    net_total = models.DecimalField('Net Total',max_digits=14, decimal_places=2, default=0)
    is_completed = models.BooleanField('Sales Created', default=False)


    def __unicode__(self):

        return str(self.delivery_note_number)

    class Meta:

        verbose_name = 'Delivery Note'
        verbose_name_plural = 'Delivery Note'


class DeliveryNoteItem(models.Model):

    item = models.ForeignKey(Item, null=True, blank=True)
    delivery_note = models.ForeignKey(DeliveryNote, null=True, blank=True)
    net_amount = models.DecimalField('Net Amount', max_digits=14, decimal_places=2, default=0)
    quantity_sold = models.IntegerField('Quantity Sold', default=0)
    selling_price = models.DecimalField('Selling Price', max_digits=14, decimal_places=2, default=0) 

    def __unicode__(self):

        return str(self.delivery_note.delivery_note_number)

    class Meta:

        verbose_name = 'Delivery Note Item'
        verbose_name_plural = 'Delivery Note Item'

class Sales(models.Model): 

    project = models.ForeignKey(Project, null=True, blank=True)
    customer = models.ForeignKey(Customer, null=True, blank=True)
    delivery_note = models.ForeignKey(DeliveryNote, null=True, blank=True)

    sales_invoice_number = models.CharField('Sales Invoice Number', null=True, blank=True, max_length=10, unique=True)
    sales_invoice_date = models.DateField('Sales Invoice Date', null=True, blank=True)

    po_no = models.CharField('P O Number', null=True, blank=True, max_length=25)
    terms = models.CharField('Terms', null=True, blank=True, max_length=200)
    rep = models.CharField('Rep', null=True, blank=True, max_length=200)
    via = models.CharField('Via', null=True, blank=True, max_length=200)
    fob = models.CharField('FOB', null=True, blank=True, max_length=200)
    
    payment_mode = models.CharField('Payment Mode', null=True, blank=True, max_length=25)
    cheque_no = models.CharField('Cheque Number',null=True, blank=True, max_length=25)
    bank_name = models.CharField('Bank Name', max_length=200,null=True, blank=True)
    bank_branch = models.CharField('Bank Branch', max_length=200, null=True, blank=True)
    cheque_date = models.DateField('Cheque Date', null=True, blank=True)
    
    net_amount = models.DecimalField('Net Amount',max_digits=14, decimal_places=2, default=0)
    round_off = models.DecimalField('Net Round Off',max_digits=14, decimal_places=2, default=0)
    grant_total = models.DecimalField('Grand Total',max_digits=14, decimal_places=2, default=0)
    balance = models.DecimalField('Balance', null=True, blank=True, decimal_places=2, default=0, max_digits=14)
    paid = models.DecimalField('Paid', null=True, blank=True, decimal_places=2, default=0, max_digits=14)
    discount_for_sale = models.DecimalField('Discount for sale',max_digits=14, decimal_places=2, default=0)
    discount_percentage_for_sale = models.DecimalField('Discount percentage for sale',max_digits=14, decimal_places=2, default=0)

    is_processed = models.BooleanField('Processed', default=False)
    def __unicode__(self):

        return str(self.sales_invoice_number)

    class Meta:

        verbose_name = 'Sales'
        verbose_name_plural = 'Sales'

class SalesItem(models.Model):

    sales = models.ForeignKey(Sales)
    item = models.ForeignKey(Item, null=True, blank=True)
    quantity_sold = models.IntegerField('Quantity Sold', default=0)
    selling_price = models.DecimalField('Selling Price', max_digits=14, decimal_places=2, default=0) 
    net_amount = models.DecimalField('Sold Net Amount', max_digits=14, decimal_places=2, default=0)
    
    
    def __unicode__(self):

        return str(self.sales.sales_invoice_number)

    class Meta:

        verbose_name = 'Sales Items'
        verbose_name_plural = 'Sales Items'

class SalesReturn(models.Model):
    sales = models.ForeignKey(Sales)
    return_invoice_number = models.IntegerField('Sales Return invoice number', unique=True)
    date = models.DateField('Date', null=True, blank=True)
    net_amount = models.DecimalField('Total', max_digits=14, decimal_places=2, default=0)
    

    def __unicode__(self):
        return str(self.sales.sales_invoice_number)

class SalesReturnItem(models.Model):
    sales_return = models.ForeignKey(SalesReturn, null=True, blank=True)
    item = models.ForeignKey(Item, null=True, blank=True)
    return_quantity = models.IntegerField('Return Quantity', null=True, blank=True)
    amount = models.DecimalField('Amount', max_digits=14, decimal_places=2, default=0)

    def __unicode__(self):

        return str(self.sales_return.return_invoice_number)

class ReceiptVoucher(models.Model):

    sales_invoice = models.ForeignKey(Sales, null=True, blank=True)
    receipt_voucher_no = models.CharField('Receipt Voucher No', null=True, blank=True, max_length=30, unique=True)
    date = models.DateField('Date', null=True, blank=True)
    total_amount = models.DecimalField('Total Amount', max_digits=14, decimal_places=2, default=0)
    paid_amount = models.DecimalField('Paid Amount', max_digits=14, decimal_places=2, default=0)
    cheque_no = models.CharField('Check Number', null=True, blank=True, max_length=50)
    bank = models.CharField('Bank', null=True, blank=True, max_length=100)
    dated = models.DateField('Dated', null=True, blank=True)
    payment_mode = models.CharField('Payment Mode', null=True, blank=True, max_length=40, choices=PAYMENT_MODE)
    
    def __unicode__(self):

        return str(self.sales_invoice.sales_invoice_number)

    class Meta:

        verbose_name = 'Receipt Voucher'
        verbose_name_plural = 'Receipt Voucher'

class CustomerAccount(models.Model):

    invoice_no = models.ForeignKey(Sales, null=True, blank=True)
    customer = models.ForeignKey(Customer, null=True, blank=True)
    total_amount = models.DecimalField('Total amount', max_digits=14, decimal_places=2, default=0)
    paid = models.DecimalField('Paid', max_digits=14, decimal_places=2, default=0)
    balance = models.DecimalField('Balance', max_digits=14, decimal_places=2, default=0)
    is_complted = models.BooleanField('Is Completed', default=False)


    class Meta:

        verbose_name = 'Customer Account'
        verbose_name_plural = 'Customer Account'

    def __unicode__(self):

        return str(self.invoice_no.sales_invoice_number)

