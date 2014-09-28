from django.db import models
from django.contrib.auth.models import User

from purchase.models import Purchase

class ExpenseHead(models.Model):
	expense_head = models.CharField('Expense Head', max_length=75, unique=True)

	class Meta:
		verbose_name_plural = 'Expense Head'

	def __unicode__(self):
		return self.expense_head

class Expense(models.Model):

	created_by = models.ForeignKey(User)
	expense_head = models.ForeignKey(ExpenseHead, null=True, blank=True)
	purchase = models.ForeignKey(Purchase, null=True, blank=True)

	voucher_no = models.IntegerField('Voucher No', unique=True)
	date = models.DateField('Date', null=True, blank=True)
	amount = models.DecimalField('Amount',max_digits=14, decimal_places=3, default=0)
	payment_mode = models.CharField('Payment Mode', null=True, blank=True, max_length=25)
	narration = models.TextField('Narration', max_length=300, null=True, blank=True)
	
	cheque_no = models.CharField('Cheque No', null=True, blank=True,max_length=200)
	cheque_date = models.DateField('Cheque Date', null=True, blank=True)
	bank_name = models.CharField('Bank Name', max_length=15, null=True, blank=True)
	branch = models.CharField('Branch', max_length=10, null=True, blank=True)
	
	class Meta:
		verbose_name_plural = 'Expense'

	def __unicode__(self):
		return self.expense_head.expense_head

