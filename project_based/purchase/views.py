import ast
import simplejson
import datetime as dt
from datetime import datetime

from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Max

from web.models import *
from purchase.models import *
from project.models import *
from expenses.models import Expense, ExpenseHead

class PurchaseEntry(View):

    def get(self, request, *args, **kwargs):

        try:
            cash_in_hand = CashInHand.objects.latest('id')
            if cash_in_hand.amount <= 0:
                cash_in_hand = None
        except:
            cash_in_hand = None
        
        purchase_type = request.GET.get('purchase_type', '')
        if purchase_type == 'project_based':
            template_name = 'purchase/purchase_entry.html'
        elif purchase_type == 'inventory_based':
            template_name = 'purchase/inventory_purchase_entry.html'
        if Purchase.objects.exists():
            invoice_number = int(Purchase.objects.aggregate(Max('purchase_invoice_number'))['purchase_invoice_number__max']) + 1
        else:
            invoice_number = 1
        if not invoice_number:
            invoice_number = 1
        return render(request, template_name,{
            'invoice_number': invoice_number,
            'cash_in_hand': cash_in_hand,
        })

    def post(self, request, *args, **kwargs):
        
        purchase_dict = ast.literal_eval(request.POST['purchase'])
        purchase, purchase_created = Purchase.objects.get_or_create(purchase_invoice_number=purchase_dict['purchase_invoice_number'])
        purchase.purchase_invoice_number = purchase_dict['purchase_invoice_number']
        purchase.supplier_invoice_number = purchase_dict['supplier_invoice_number']
        purchase.supplier_do_number = purchase_dict['supplier_do_number']
        purchase.supplier_invoice_date = datetime.strptime(purchase_dict['supplier_invoice_date'], '%d/%m/%Y')
        purchase.purchase_invoice_date = datetime.strptime(purchase_dict['purchase_invoice_date'], '%d/%m/%Y')
        
        purchase.payment_mode = purchase_dict['payment_mode']
        if purchase_dict['payment_mode'] == 'cash' or purchase_dict['payment_mode'] == 'cheque':
            purchase.is_paid_completely = True 
        if purchase_dict['bank_name']:
            purchase.bank_name = purchase_dict['bank_name']
        if purchase_dict['cheque_no']:
            purchase.cheque_no = purchase_dict['cheque_no']
        if purchase_dict['cheque_date']:
            purchase.cheque_date = datetime.strptime(purchase_dict['cheque_date'], '%d/%m/%Y')
        supplier = Supplier.objects.get(name=purchase_dict['supplier_name']) 
        if purchase_dict['transport'] != 'other' or purchase_dict['transport'] != 'select' or purchase_dict['transport'] != '': 
            try:     
                transport = TransportationCompany.objects.get(company_name=purchase_dict['transport'])
                purchase.transportation_company = transport
            except:
                pass
        purchase.supplier = supplier
        
        if purchase_dict['discount']:
            purchase.discount = purchase_dict['discount']
        else:
            purchase.discount = 0
        if purchase_dict['discount_percentage']:
            purchase.discount_percentage = purchase_dict['discount_percentage']
        else:
            purchase.discount_percentage = 0
        purchase.net_total = purchase_dict['net_total']
        purchase.purchase_expense = purchase_dict['purchase_expense']
        purchase.grant_total = purchase_dict['grant_total']
        if purchase_dict['payment_mode'] == 'credit':
            supplier_account, supplier_account_created = SupplierAccount.objects.get_or_create(supplier=supplier)
            if supplier_account_created:
                supplier_account.total_amount = purchase_dict['supplier_amount']
                supplier_account.balance = purchase_dict['supplier_amount']
            else:
                if purchase_created:
                    supplier_account.total_amount = supplier_account.total_amount + purchase_dict['supplier_amount']
                    supplier_account.balance = supplier_account.balance + purchase_dict['supplier_amount']
                else:
                    supplier_account.total_amount = supplier_account.total_amount - purchase.supplier_amount + purchase_dict['supplier_amount']
                    supplier_account.balance = supplier_account.balance - purchase.supplier_amount + purchase_dict['supplier_amount']
            supplier_account.save()       
            purchase.supplier_amount = purchase_dict['supplier_amount']
            purchase.save()
        try:
            cash_in_hand = CashInHand.objects.latest('id')
        except Exception:
            cash_in_hand = None
        if cash_in_hand:
            cash_in_hand.amount = float(cash_in_hand.amount) - (float(purchase_dict['purchase_expense']) + float(purchase_dict['supplier_amount']))
            cash_in_hand.save()

            cash_entry = CashEntry.objects.create(cash_in_hand=cash_in_hand)
            cash_entry.in_out = 'out'
            cash_entry.date = datetime.strptime(purchase_dict['purchase_invoice_date'], '%d/%m/%Y')
            cash_entry.from_to = 'Purchase'
            cash_entry.amount = purchase_dict['supplier_amount'] 
            cash_entry.purpose = 'other'
            cash_entry.other_purpose = 'Purchase'
            cash_entry.purchase = purchase
            cash_entry.save()


        if purchase_dict['purchase_mode'] == 'project_purchase':
            project = Project.objects.get(id=purchase_dict['project_id'])
        else:
            project = None
        if project and cash_in_hand:
            cash_entry.project = project
            cash_entry.save()
        if float(purchase_dict['purchase_expense']) > 0:
            # Save purchase_expense in Expense
            try: 
                expense = Expense.objects.get(purchase=purchase)
            except:
                if Expense.objects.exists():
                    voucher_no = int(Expense.objects.aggregate(Max('voucher_no'))['voucher_no__max']) + 1
                else:
                    voucher_no = 1
                if not voucher_no:
                    voucher_no = 1
                expense = Expense.objects.create(purchase=purchase, created_by=request.user, voucher_no=voucher_no, project=project)
            expense.created_by = request.user
            expense.expense_head, created = ExpenseHead.objects.get_or_create(expense_head = 'purchase')
            expense.date = dt.datetime.now().date().strftime('%Y-%m-%d')
            expense.amount = purchase_dict['purchase_expense']
            expense.payment_mode = 'cash'
            expense.narration = 'By purchase'

            cash_entry = CashEntry.objects.create(cash_in_hand=cash_in_hand)
            cash_entry.in_out = 'out'
            cash_entry.date = datetime.strptime(purchase_dict['purchase_invoice_date'], '%d/%m/%Y')
            cash_entry.from_to = 'Purchase Expense'
            cash_entry.amount = purchase_dict['purchase_expense']
            cash_entry.purpose = 'other'
            cash_entry.other_purpose = 'Purchase Expense'
            cash_entry.purchase = purchase
            cash_entry.save()
            cash_entry.expense = expense
            cash_entry.save()
            expense.save()
            if project:
                expense.project = project
                expense.save()
        purchase_items = purchase_dict['purchase_items']
        deleted_items = purchase_dict['deleted_items']

        if project:
            purchase.project = project
            project.purchase_amount = float(project.purchase_amount) + float(purchase.grant_total)
            project.expense_amount = float(project.expense_amount) + float(purchase_dict['purchase_expense'])
            project.save()
        purchase.save()
        
        for purchase_item in purchase_items:

            item = Item.objects.get(code=purchase_item['item_code'])
            p_item, item_created = PurchaseItem.objects.get_or_create(item=item, purchase=purchase)
            if project:
                project_item, project_item_created = ProjectItem.objects.get_or_create(project=project, item=item)
                if project_item_created:
                    project_item.quantity = int(purchase_item['qty_purchased'])                
                else:
                    print 'project_item.quantity=', project_item.quantity
                    print "purchase_item['qty_purchased']=", purchase_item['qty_purchased']
                    if purchase_created:
                        project_item.quantity = project_item.quantity + int(purchase_item['qty_purchased'])
                    else:
                        project_item.quantity = project_item.quantity - p_item.quantity_purchased + int(purchase_item['qty_purchased'])
                project_item.selling_price = purchase_item['selling_price']
                project_item.unit_price = purchase_item['unit_price']
                project_item.save()              
            item = Item.objects.get(code=purchase_item['item_code'])
            inventory, created = InventoryItem.objects.get_or_create(item=item)
            if created:
                inventory.quantity = int(purchase_item['qty_purchased'])                
            else:
                if purchase_created:
                    inventory.quantity = inventory.quantity + int(purchase_item['qty_purchased'])
                else:
                    inventory.quantity = inventory.quantity - p_item.quantity_purchased + int(purchase_item['qty_purchased'])
            inventory.selling_price = purchase_item['selling_price']
            inventory.unit_price = purchase_item['unit_price']
            inventory.save()    
            p_item.purchase = purchase
            p_item.item = item
            p_item.quantity_purchased = purchase_item['qty_purchased']
            p_item.cost_price = purchase_item['cost_price']
            p_item.net_amount = purchase_item['net_amount']
            p_item.save()
                    
        res = {
            'result': 'Ok',
        } 

        response = simplejson.dumps(res)
        status_code = 200
        return HttpResponse(response, status = status_code, mimetype="application/json")

class PurchaseDetails(View):

    def get(self, request, *args, **kwargs):
        status_code = 200
        if request.is_ajax():
            try:
                invoice_number = request.GET.get('purchase_invoice_no', '')
                purchase  = Purchase.objects.get(purchase_invoice_number=int(invoice_number))
                items_list = []
                for item in purchase.purchaseitem_set.all():
                    current_stock = 0
                    selling_price = 0
                    unit_price = 0
                    if purchase.project:
                        project_item = ProjectItem.objects.filter(project=purchase.project, item=item.item)
                        current_stock = project_item[0].quantity
                        unit_price = project_item[0].unit_price
                        selling_price = project_item[0].selling_price
                    else:
                        inventory = InventoryItem.objects.filter(item=item.item)
                        current_stock = inventory[0].quantity
                        unit_price = inventory[0].unit_price
                        selling_price = inventory[0].selling_price
                    items_list.append({
                        'item_code': item.item.code,
                        'item_name': item.item.name,
                        
                        'current_stock': current_stock,
                                        
                        'selling_price': selling_price,
                        'qty_purchased': item.quantity_purchased,
                        'cost_price': unit_price,
                        'net_amount': item.net_amount,
                        'unit_price': unit_price,
                    })

                purchase_dict = {
                    'purchase_invoice_number': purchase.purchase_invoice_number,
                    'supplier_invoice_number': purchase.supplier_invoice_number,
                    'supplier_do_number': purchase.supplier_do_number,
                    'supplier_name': purchase.supplier.name,
                    'transport': purchase.transportation_company.company_name if purchase.transportation_company else '',
                    'supplier_invoice_date': purchase.supplier_invoice_date.strftime('%d/%m/%Y'),
                    'purchase_invoice_date': purchase.purchase_invoice_date.strftime('%d/%m/%Y'), 
                    'purchase_items': items_list,
                    'supplier_amount': purchase.supplier_amount,
                    'net_total': purchase.net_total,
                    'purchase_expense': purchase.purchase_expense,
                    'discount': purchase.discount,
                    'grant_total': purchase.grant_total,
                    'project_id': purchase.project.id if purchase.project else '',
                    'project_name':  purchase.project.id if purchase.project else '',
                    'discount_percentage': purchase.discount_percentage,
                    'payment_mode': purchase.payment_mode,
                }
                res = {
                    'result': 'Ok',
                    'purchase': purchase_dict
                } 
                response = simplejson.dumps(res)
                status_code = 200
            except Exception as ex:
                print str(ex)
                res = {
                    'result': 'error',
                    'purchase': {}
                } 
                response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")
        return render(request, 'purchase/purchase_details.html', {})