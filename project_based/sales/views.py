# -*- coding: utf-8 -*- 
import ast
import simplejson
import datetime as dt
from datetime import datetime
from decimal import *


from django.db.models import Max
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.conf import settings

from sales.models import *
from project.models import *
from web.models import *

from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import green, black, red
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_JUSTIFY, TA_CENTER
from reportlab.platypus import Paragraph, Table, TableStyle

from smartbook_new import arabic_reshaper

path = settings.PROJECT_ROOT.replace("\\", "/")+"/header/images/Logo.jpg"

font_path_regular = settings.PROJECT_ROOT.replace("\\", "/")+"/header/AdobeArabic-Regular.ttf"
font_path_bold = settings.PROJECT_ROOT.replace("\\", "/")+"/header/AdobeArabic-Bold.ttf"
pdfmetrics.registerFont(TTFont('Arabic-normal', font_path_regular))
pdfmetrics.registerFont(TTFont('Arabic-bold', font_path_bold))


style = [
    ('FONTSIZE', (0,0), (-1, -1), 13),
    ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
]

para_style = ParagraphStyle('fancy')
para_style.fontSize = 13
para_style.fontName = 'Helvetica'

def header(canvas, y):

    canvas.setFont("Arabic-bold", 40)  
    canvas.setFillColor(red)
    solutions_text = arabic_reshaper.reshape(u'المعلومات')
    canvas.drawString(620, y + 25, solutions_text[::-1])
    canvas.setFillColor(black)
    it_text = arabic_reshaper.reshape(u'لحلول تقنية')
    canvas.drawString(750, y + 25, it_text[::-1])
    canvas.setFillColor(green)
    indusco_text = arabic_reshaper.reshape(u'اندسكو')
    canvas.drawString(880, y + 25, indusco_text[::-1])

    canvas.setFont("Helvetica", 40)  
    canvas.setFillColor(green)
    canvas.drawString(50, y + 21, 'Indusco')
    canvas.setFillColor(black)
    canvas.drawString(200, y + 21, 'IT')
    canvas.setFillColor(red)
    canvas.drawString(250, y + 21, 'Solutions')
    canvas.setFillColor(black)
    canvas.drawImage(path, 50, y, width=33*cm, height=3*cm, preserveAspectRatio=True)

    canvas.setFont("Helvetica", 14)  
    canvas.drawString(50, y - 15, 'P.O Box: 7307, Abu Dhabi - United Arab Emirates')
    canvas.drawString(50, y - 35, 'Tel: +97125507474, Fax: +97126777009')

    canvas.setFont('Arabic-normal', 18)
    po_box_place_text = arabic_reshaper.reshape(u'صندوق بريد : ۷۰۳۷ أبوظبي الإمارات العربية المتحدة')
    canvas.drawString(700, y - 15, po_box_place_text[::-1])

    fax_text = arabic_reshaper.reshape(u'فاكس')
    canvas.drawString(795, y - 35, fax_text[::-1])
    fax_no = arabic_reshaper.reshape(u'+۹۷۱۲ ٦۷۷۷۰۰۹: ')
    canvas.drawString(710, y - 35, fax_no)
    tel_text = arabic_reshaper.reshape(u'الهاتف')
    canvas.drawString(920, y - 35, tel_text[::-1])
    tel_no = arabic_reshaper.reshape(u', +۹۷۱۲ ۵۵۰۷٤۷٤: ')
    canvas.drawString(825, y - 35, tel_no)

    return canvas

def footer(canvas, y):

    canvas.setFont('Times-Roman', 14)
    canvas.line(50, y - 1050, 450, y - 1050)
    canvas.line(50, y - 1170, 450, y - 1170)
    canvas.line(50, y - 1050, 50, y - 1170)
    canvas.line(450, y - 1050, 450, y - 1170)

    canvas.drawString(60, y - 1070, 'Reciever Name :')
    canvas.drawString(60, y - 1150, 'Signature          :')

    canvas.line(650, y - 1050, 950, y - 1050)
    canvas.line(650, y - 1170, 950, y - 1170)
    canvas.line(650, y - 1050, 650, y - 1170)
    canvas.line(950, y - 1050, 950, y - 1170)

    canvas.drawString(660, y - 1070, 'FOR INDUSCO IT SOLUTIONS ')
    canvas.drawString(660, y - 1150, 'Signature ')

    
    return canvas
   

def invoice_body_layout(canvas, y, sales):

    canvas.setFont("Helvetica-Bold", 40)  
    canvas.drawString(440, y - 80, 'Invoice')

    canvas.setFont("Helvetica", 15)

    # Date and Invoice Box start
    canvas.line(700, y - 45, 950, y - 45)
    canvas.line(700, y - 100, 950, y - 100)  
    canvas.line(700, y - 70, 950, y - 70)  

    canvas.line(700, y - 45, 700, y - 100)  
    canvas.line(950, y - 45, 950, y - 100)
    canvas.line(825, y - 45, 825, y - 100)
    # Date and Invoice Box end

    # Bill and Ship Box start

    canvas.line(50, y - 130, 400, y - 130)
    canvas.line(50, y - 160, 400, y - 160)
    canvas.line(50, y - 250, 400, y - 250)

    canvas.line(500, y - 130, 900, y - 130)
    canvas.line(500, y - 160, 900, y - 160)
    canvas.line(500, y - 250, 900, y - 250)
    
    canvas.line(50, y - 130, 50, y - 250)  
    canvas.line(400, y - 130, 400, y - 250)
    canvas.line(500, y - 130, 500, y - 250)  
    canvas.line(900, y - 130, 900, y - 250)

    # Bill and Ship Box end

    canvas.setFont("Helvetica", 14)
    canvas.drawString(745,  y - 60, 'Date')
    canvas.drawString(865,  y - 60, 'Invoice #')

    canvas.drawString(100, y - 150, 'Bill To')
    canvas.drawString(550, y - 150, 'Ship To')

    # Item Top Box start
    canvas.line(50, y - 270, 950, y - 270)  
    canvas.line(50, y - 300, 950, y - 300)
    canvas.line(50, y - 340, 950, y - 340) 

    canvas.line(50, y - 270, 50, y - 980) 
    canvas.line(150, y - 270, 150, y - 340) 
    canvas.line(300, y - 270, 300, y - 340)
    canvas.line(380, y - 270, 380, y - 340)
    canvas.line(480, y - 270, 480, y - 340)
    canvas.line(600, y - 270, 600, y - 340)
    canvas.line(750, y - 270, 750, y - 340)
    canvas.line(950, y - 270, 950, y - 980) 

    # Item Top Box end
    canvas.drawString(60, y - 290, 'P.O.Number')
    canvas.drawString(200, y - 290, 'Terms')
    canvas.drawString(320, y - 290, 'Rep')
    canvas.drawString(415, y - 290, 'Ship')
    canvas.drawString(530, y - 290, 'Via')
    canvas.drawString(650, y - 290, 'F.O.B')
    canvas.drawString(820, y - 290, 'Project')

    # Item Box start
    canvas.line(50, y - 370, 950, y - 370) 
    
    canvas.line(150, y - 340, 150, y - 980) 
    canvas.line(300, y - 340, 300, y - 980)
    canvas.line(675, y - 340, 675, y - 980)  
    canvas.line(815, y - 340, 815, y - 980) 

    canvas.line(50, y - 980, 950, y - 980)
    

    canvas.drawString(60, y - 360, 'Quantity')
    canvas.drawString(190, y - 360, 'Item Code')
    canvas.drawString(450, y - 360, 'Item Name')
    canvas.drawString(710, y - 360, 'Price Each')
    canvas.drawString(850, y - 360, 'Amount')

    canvas.drawString(725,  y - 85, sales.sales_invoice_date.strftime('%d-%b-%Y'))
    canvas.drawString(865,  y - 85, sales.sales_invoice_number)

    canvas.drawString(70, y - 180, sales.customer.customer_name)
    canvas.drawString(70, y - 200, sales.customer.house_name)
    canvas.drawString(70, y - 220, sales.customer.street)
    # canvas.drawString(250, y - 220, ',' if sales.customer.city and sales.customer.street else '')
    canvas.drawString(260, y - 220, sales.customer.city)

    canvas.drawString(510, y - 180, sales.customer.customer_name)
    canvas.drawString(510, y - 200, sales.customer.house_name)
    canvas.drawString(510, y - 220, sales.customer.street)
    # canvas.drawString(705, y - 220, ',' if sales.customer.city and sales.customer.street else '')
    canvas.drawString(715, y - 220, sales.customer.city)


    canvas.setFont('Times-Roman', 14)
    canvas.drawString(60, y - 330, sales.po_no if sales.po_no else '')
    canvas.drawString(180, y - 330, sales.terms if sales.terms else '')
    canvas.drawString(310, y - 330, sales.rep if sales.rep else '')
    canvas.drawString(400, y - 330, sales.sales_invoice_date.strftime('%d-%b-%Y'))
    canvas.drawString(500, y - 330, sales.via if sales.via else '')
    canvas.drawString(620, y - 330, sales.fob if sales.fob else '')
    canvas.drawString(800, y - 330, (sales.project.name if sales.project else ''))

    return canvas 

def dn_body_layout(canvas, y, delivery_note):

    canvas.setFont("Helvetica-Bold", 40)  
    canvas.drawString(350, y - 180, 'Delivery Note')
    canvas.setFont("Helvetica", 15)

    # Date and Invoice Box start
    canvas.line(700, y - 45, 950, y - 45)
    canvas.line(700, y - 100, 950, y - 100)  
    canvas.line(700, y - 70, 950, y - 70)  

    canvas.line(700, y - 45, 700, y - 100)  
    canvas.line(950, y - 45, 950, y - 100)
    canvas.line(825, y - 45, 825, y - 100)
    # Date and Invoice Box end

    canvas.setFont("Helvetica", 14)
    canvas.drawString(745,  y - 60, 'Date')
    canvas.drawString(865,  y - 60, 'DN No #')

    canvas.drawString(725,  y - 85, delivery_note.date.strftime('%d-%b-%Y') if delivery_note.date else '')
    canvas.drawString(865,  y - 85, delivery_note.delivery_note_number)

    canvas.line(200, y - 270, 825, y - 270)  

    canvas.line(200, y - 270, 200, y - 980) 

    canvas.line(200, y - 300, 825, y - 300) 
    
    canvas.line(300, y - 270, 300, y - 980) 
    canvas.line(450, y - 270, 450, y - 980)
    canvas.line(825, y - 270, 825, y - 980)  

    canvas.line(200, y - 980, 825, y - 980)

    canvas.drawString(210, y - 290, 'Quantity')
    canvas.drawString(340, y - 290, 'Item Code')
    canvas.drawString(600, y - 290, 'Item Name')

    return canvas


class SalesEntry(View):
    def get(self, request, *args, **kwargs):
        
        sales_type = request.GET.get('sales_type', '')

        if sales_type == 'project_sales':
            template_name = 'sales/sales_entry.html'
        elif sales_type == 'dn_sales':
            template_name = 'sales/DN_sales_entry.html'
        elif sales_type == 'inventory_sales':
            template_name = 'sales/inventory_sales_entry.html'
        current_date = dt.datetime.now().date()

        inv_number = Sales.objects.aggregate(Max('id'))['id__max']

        if not inv_number:
            inv_number = 1
        else:
            inv_number = inv_number + 1
        
        invoice_number = 'INV' + str(inv_number)
        return render(request, template_name,{
            'sales_invoice_number': invoice_number,
            'current_date': current_date.strftime('%d/%m/%Y'),
        })


    def post(self, request, *args, **kwargs):

        sales_dict = ast.literal_eval(request.POST['sales'])
        sales, sales_created = Sales.objects.get_or_create(sales_invoice_number=sales_dict['sales_invoice_number'])
        project = None

        if sales_dict['sales_mode'] == 'project_direct' or sales_dict['sales_mode'] == 'inventory_sales':
            customer = Customer.objects.get(customer_name=sales_dict['customer'])
            sales.customer = customer
        sales.sales_invoice_number = sales_dict['sales_invoice_number']
        sales.payment_mode = sales_dict['payment_mode']
        
        sales.sales_invoice_date = datetime.strptime(sales_dict['sales_invoice_date'], '%d/%m/%Y')
        
        sales.discount_for_sale = sales_dict['discount']
        sales.discount_percentage_for_sale = sales_dict['discount_percentage']
        sales.round_off = sales_dict['roundoff']
        sales.net_amount = sales_dict['net_total']
        sales.grant_total = sales_dict['grant_total']
        sales.paid = sales_dict['paid']

        sales.po_no = sales_dict['po_no']
        sales.terms = sales_dict['terms']
        sales.rep = sales_dict['rep']
        sales.via = sales_dict['via']
        sales.fob = sales_dict['fob']

        if sales_dict['payment_mode'] == 'cheque':
            sales.cheque_no = sales_dict['cheque_no'] 
            sales.bank_name = sales_dict['bank_name']
            sales.bank_branch = sales_dict['branch']
            sales.cheque_date = datetime.strptime(sales_dict['cheque_date'], '%d/%m/%Y')

        if sales_dict['payment_mode'] == 'cheque' or sales_dict['payment_mode'] == 'cash':
            sales.is_processed = True
            sales.paid = sales_dict['grant_total']
        sales.balance = float(sales.grant_total) - float(sales.paid)
        sales.save()

        sales_items = sales_dict['sales_items']
        removed_items = sales_dict['removed_items']
        if sales_dict['sales_mode'] == 'project_direct':
            project = Project.objects.get(id=int(sales_dict['project_id']))
            sales.project=project
            project.sales_amount =  float(project.sales_amount) + float(sales.grant_total)
            project.save()
        elif sales_dict['sales_mode'] == 'dn_sales':
            delivery_note = DeliveryNote.objects.get(id=sales_dict['dn_id'])
            sales.delivery_note = delivery_note
            if delivery_note.project:
                sales.project = delivery_note.project
                project = delivery_note.project
                project.sales_amount =  float(project.sales_amount) + float(sales.grant_total)
                project.save()
            sales.customer = delivery_note.customer
            delivery_note.is_completed = True
            delivery_note.save()
        sales.save()

        for r_item in removed_items:
            item = Item.objects.get(code=r_item['item_code'])
            if item.item_type == 'item':
                if sales_dict['sales_mode'] == 'dn_sales':
                    d_item = DeliveryNoteItem.objects.get(id=r_item['id'])
                    if d_item.delivery_note.project:
                        project_item = ProjectItem.objects.get(item=d_item.item, project=d_item.delivery_note.project)
                        project_item.quantity = int(project_item.quantity) + int(r_item['qty_sold'])
                        project_item.save()
                    inventory = InventoryItem.objects.get(item=d_item.item)
                    inventory.quantity = int(inventory.quantity) + int(r_item['qty_sold'])
                    inventory.save()
        for sales_item in sales_items:
            item = Item.objects.get(code=sales_item['item_code'])
            s_item, item_created = SalesItem.objects.get_or_create(item=item, sales=sales)
            if item.item_type == 'item':
                inventory = InventoryItem.objects.get(item=item)
                if sales_dict['sales_mode'] == 'project_direct':
                    if item.item_type == 'item':
                        project_item = ProjectItem.objects.get(item=item, project=project)
                        if sales_created:
                            project_item.quantity = project_item.quantity - int(sales_item['qty_sold'])
                            inventory.quantity = inventory.quantity - int(sales_item['qty_sold'])
                        else:
                            project_item.quantity = project_item.quantity + s_item.quantity_sold - int(sales_item['qty_sold'])  
                            inventory.quantity = int(inventory.quantity) + int(s_item.quantity_sold) - int(sales_item['qty_sold'])    
                        inventory.save()
                        project_item.save()
                elif sales_dict['sales_mode'] == 'dn_sales':
                    d_item = DeliveryNoteItem.objects.get(id=sales_item['id'])
                    
                    # Update Quantity
                    if item.item_type == 'item':
                        if int(d_item.quantity_sold) != int(sales_item['qty_sold']):
                            if d_item.delivery_note.project:
                                project_item = ProjectItem.objects.get(item=item, project=d_item.delivery_note.project)
                                project_item.quantity = int(project_item.quantity) + int(d_item.quantity_sold) - int(sales_item['qty_sold'])
                                project_item.save()
                            inventory = InventoryItem.objects.get(item=d_item.item)
                            inventory.quantity = int(inventory.quantity) + int(d_item.quantity_sold) - int(sales_item['qty_sold'])
                            inventory.save()
                elif sales_dict['sales_mode'] == 'inventory_sales':
                    
                    if item.item_type == 'item':
                        if item_created:
                            inventory.quantity = inventory.quantity - int(sales_item['qty_sold'])
                        else:
                            inventory.quantity = int(inventory.quantity) + int(s_item.quantity_sold) - int(sales_item['qty_sold'])      
                        inventory.save()
                    project_items = ProjectItem.objects.filter(item=inventory.item)
                    for pt in project_items:
                        if pt.quantity > inventory.quantity:
                            pt.quantity = inventory.quantity
                            pt.save()

            s_item.quantity_sold = sales_item['qty_sold']
            s_item.net_amount = sales_item['net_amount']
            s_item.selling_price = sales_item['unit_price']
            s_item.save()

        res = {
            'result': 'Ok',
            'id': sales.id,
        }
        response = simplejson.dumps(res)
        status_code = 200
        return HttpResponse(response, status = status_code, mimetype="application/json")

class ReceiptVoucherView(View):

    def get(self, request, *args, **kwargs):
        current_date = dt.datetime.now().date()
        voucher_no = ReceiptVoucher.objects.aggregate(Max('id'))['id__max']
        prefix = 'RV'
        if not voucher_no:
            voucher_no = 1
        else:
            voucher_no = voucher_no + 1
        voucher_no = prefix + str(voucher_no)

        return render(request, 'sales/receipt_voucher.html',{
            'current_date': current_date.strftime('%d/%m/%Y'),
            'voucher_no': voucher_no,
        })
    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            receiptvoucher = ast.literal_eval(request.POST['receiptvoucher'])
            customer = Customer.objects.get(customer_name=receiptvoucher['customer'])
            sales_invoice_obj = Sales.objects.get(sales_invoice_number=receiptvoucher['invoice_no'])
            receipt_voucher = ReceiptVoucher.objects.create(sales_invoice=sales_invoice_obj)

            receipt_voucher.date = datetime.strptime(receiptvoucher['date'], '%d/%m/%Y')
            
            receipt_voucher.total_amount = receiptvoucher['amount']
            receipt_voucher.paid_amount = receiptvoucher['paid_amount']
            receipt_voucher.receipt_voucher_no = receiptvoucher['voucher_no']
            receipt_voucher.payment_mode = receiptvoucher['payment_mode']
            receipt_voucher.bank = receiptvoucher['bank_name']
            receipt_voucher.cheque_no = receiptvoucher['cheque_no']
            if receiptvoucher['cheque_date']:   
                receipt_voucher.dated = datetime.strptime(receiptvoucher['cheque_date'], '%d/%m/%Y')
            receipt_voucher.save()
            customer_account, created = CustomerAccount.objects.get_or_create(customer=customer, invoice_no=sales_invoice_obj )
 
            if created:
                customer_account.total_amount = receiptvoucher['amount']
                customer_account.paid = receiptvoucher['paid_amount']
            else:
                customer_account.total_amount = receiptvoucher['amount']
                customer_account.paid = float(customer_account.paid) + float(receiptvoucher['paid_amount'])
            customer_account.save()
            customer_account.balance = float(customer_account.total_amount) - float(customer_account.paid)
            customer_account.save()
            sales_invoice_obj.balance = customer_account.balance
            sales_invoice_obj.save()
            if customer_account.balance == 0:
                customer_account.is_complted = True
                customer_account.save()
                sales_invoice_obj.is_processed = True
                sales_invoice_obj.save()
           
            res = {
                'result': 'OK',
                'receiptvoucher_id': receipt_voucher.id,
            }

            response = simplejson.dumps(res)

            return HttpResponse(response, status=200, mimetype='application/json')  


class InvoiceDetails(View):

    def get(self, request, *args, **kwargs):
        invoice_no = request.GET.get('invoice_no', '')
        ctx_rv_invoice_details = []
        ctx_invoice_details = []
        ctx_whole_invoices = []
        invoice_details = Sales.objects.filter(sales_invoice_number__istartswith=invoice_no, is_processed=False, payment_mode='credit')
        try:
            invoices = Sales.objects.filter(sales_invoice_number__istartswith=invoice_no, is_processed=False)
        except Exception as ex:
            invoices = []
        whole_invoices = Sales.objects.filter(sales_invoice_number=invoice_no)
        status = 200
        for invoice in invoice_details:
            customer_account, created = CustomerAccount.objects.get_or_create(customer=invoice.customer, invoice_no=invoice)
            ctx_rv_invoice_details.append({
                'invoice_no': invoice.sales_invoice_number if invoice else '',
                'invoice_date': invoice.sales_invoice_date.strftime('%d/%m/%Y') if invoice else '',
                'amount': float(invoice.grant_total) - float(invoice.paid) if invoice else '',
                'customer': invoice.customer.customer_name if invoice.customer else '',
                'paid_amount': customer_account.paid if customer_account.paid else 0,
            })
        for invoice in invoices:
            ctx_item_list = []
            current_stock = 0
            for s_item in invoice.salesitem_set.all():
                if s_item.item.item_type == 'item':
                    if invoice.delivery_note and not invoice.project or not invoice.project and not invoice.delivery_note:
                        inventory = InventoryItem.objects.get(item=s_item.item)
                        current_stock = inventory.quantity
                    elif invoice.delivery_note and invoice.project or invoice.project and not invoice.delivery_note:
                        project_item = ProjectItem.objects.get(item=s_item.item, project=invoice.project)
                        current_stock = project_item.quantity
                ctx_item_list.append({
                    'item_name': s_item.item.name,
                    'item_code': s_item.item.code,
                    'current_stock': current_stock,
                    'unit_price': s_item.selling_price,
                    'qty_sold': s_item.quantity_sold,
                    'net_amount': s_item.net_amount,
                })
                current_stock = 0
            ctx_invoice_details.append({
                'invoice_no': invoice.sales_invoice_number,
                'date': invoice.sales_invoice_date.strftime('%d/%m/%Y') if invoice.sales_invoice_date else '',
                'customer': invoice.customer.customer_name,
                'payment_mode': invoice.payment_mode,
                'net_total': invoice.net_amount,
                'grant_total': invoice.grant_total,
                'discount_sale': invoice.discount_for_sale,
                'discount_percentage': invoice.discount_percentage_for_sale,
                'roundoff': invoice.round_off,
                'paid': invoice.paid,
                'balance': invoice.balance,
                'project_name': invoice.project.name if invoice.project else '',
                'delivery_note_no': invoice.delivery_note.delivery_note_number if invoice.delivery_note else '',
                'lpo_number': invoice.delivery_note.lpo_number if invoice.delivery_note else '',
                'sales_items': ctx_item_list,
                'po_no': invoice.po_no if invoice.po_no else '',
                'terms': invoice.terms if invoice.terms else '',
                'rep': invoice.rep if invoice.rep else '',
                'via': invoice.via if invoice.via else '',
                'fob': invoice.fob if invoice.fob else '',
            })
        for invoice in whole_invoices:
            ctx_item_list = []
            current_stock = 0
            for s_item in invoice.salesitem_set.all():
                if s_item.item.item_type == 'item':
                    if invoice.delivery_note and not invoice.project or not invoice.project and not invoice.delivery_note:
                        inventory = InventoryItem.objects.get(item=s_item.item)
                        current_stock = inventory.quantity
                    elif invoice.delivery_note and invoice.project or invoice.project and not invoice.delivery_note:
                        project_item = ProjectItem.objects.get(item=s_item.item, project=invoice.project)
                        current_stock = project_item.quantity
                ctx_item_list.append({
                    'item_name': s_item.item.name,
                    'item_code': s_item.item.code,
                    'current_stock': current_stock,
                    'unit_price': s_item.selling_price,
                    'qty_sold': s_item.quantity_sold,
                    'net_amount': s_item.net_amount,
                })
                current_stock = 0
            ctx_whole_invoices.append({
                'id': invoice.id,
                'invoice_no': invoice.sales_invoice_number,
                'date': invoice.sales_invoice_date.strftime('%d/%m/%Y') if invoice.sales_invoice_date else '',
                'customer': invoice.customer.customer_name,
                'payment_mode': invoice.payment_mode,
                'net_total': invoice.net_amount,
                'grant_total': invoice.grant_total,
                'discount_sale': invoice.discount_for_sale,
                'discount_percentage': invoice.discount_percentage_for_sale,
                'roundoff': invoice.round_off,
                'paid': invoice.paid,
                'balance': invoice.balance,
                'project_name': invoice.project.name if invoice.project else '',
                'dn_no': invoice.delivery_note.delivery_note_number if invoice.delivery_note else '',
                'lpo_no': invoice.delivery_note.lpo_number if invoice.delivery_note else '',
                'sales_items': ctx_item_list,
                'po_no': invoice.po_no if invoice.po_no else '',
                'terms': invoice.terms if invoice.terms else '',
                'rep': invoice.rep if invoice.rep else '',
                'via': invoice.via if invoice.via else '',
                'fob': invoice.fob if invoice.fob else '',
            })

        res = {
            'result': 'ok',
            'rv_invoice_details': ctx_rv_invoice_details,
            'sales_invoices': ctx_invoice_details,
            'whole_invoices': ctx_whole_invoices,
        }
        response = simplejson.dumps(res)

        return HttpResponse(response, status=status, mimetype='application/json')

class DeliveryNoteDetails(View):

    def get(self, request, *args, **kwargs):

        status = 200
        dn_no = request.GET.get('dn_no', '')
        try:
            delivery_notes = DeliveryNote.objects.filter(delivery_note_number=dn_no, is_completed=False)
        except Exception as ex:
            delivery_notes = []
        try:
            whole_delivery_notes = DeliveryNote.objects.filter(delivery_note_number=dn_no)
        except Exception as ex:
            whole_delivery_notes = []
        ctx_dn_details = []
        ctx_whole_dn_details = []
        for delivery_note in delivery_notes:
            i = 0
            i = i + 1
            ctx_item_list = []
            if delivery_note.deliverynoteitem_set.all().count() > 0:
                for d_item in delivery_note.deliverynoteitem_set.all():
                    current_stock = 0
                    if d_item.item.item_type == 'item': 
                        if delivery_note.project:
                            p_item = ProjectItem.objects.get(project=delivery_note.project, item=d_item.item)
                            current_stock = p_item.quantity
                        else:
                            inventory, created = InventoryItem.objects.get_or_create(item=d_item.item)
                            current_stock = inventory.quantity
                    ctx_item_list.append({
                        'sl_no': i,
                        'id': d_item.id,
                        'name': d_item.item.name if d_item.item else '',
                        'type': d_item.item.item_type if d_item.item else '',
                        'item_code': d_item.item.code if d_item.item else '',
                        'qty_sold': d_item.quantity_sold,
                        'current_stock': current_stock,
                        'selling_price': d_item.selling_price,
                        'net_amount': d_item.net_amount,
                        'unit_price': d_item.selling_price,
                    })
                    i = i + 1
            ctx_dn_details.append({
                'id': delivery_note.id,
                'dn_no': delivery_note.delivery_note_number,
                'lpo_no': delivery_note.lpo_number,
                'project_name': delivery_note.project.name if delivery_note.project else '',
                'project_id': delivery_note.project.id if delivery_note.project else '',
                'sales_items': ctx_item_list,
                'date': delivery_note.date.strftime('%d/%m/%Y') if delivery_note.date else '',
                'customer': delivery_note.customer.customer_name if delivery_note.customer else '',
                'net_total': delivery_note.net_total,
                'is_project': 'true' if delivery_note.project else 'false',
            })
        for delivery_note in whole_delivery_notes:
            i = 0
            i = i + 1
            ctx_item_list = []
            if delivery_note.deliverynoteitem_set.all().count() > 0:
                for d_item in delivery_note.deliverynoteitem_set.all():
                    current_stock = 0
                    if d_item.item.item_type == 'item':
                        if delivery_note.project:
                            p_item = ProjectItem.objects.get(project=delivery_note.project, item=d_item.item)
                            current_stock = p_item.quantity
                        else:
                            inventory, created = InventoryItem.objects.get_or_create(item=d_item.item)
                            current_stock = inventory.quantity
                    ctx_item_list.append({
                        'sl_no': i,
                        'name': d_item.item.name if d_item.item else '',
                        'code': d_item.item.code if d_item.item else '',
                        'type': d_item.item.item_type if d_item.item else '',
                        'qty_sold': d_item.quantity_sold,
                        'current_stock': current_stock,
                        'selling_price': d_item.selling_price,
                        'net_amount': d_item.net_amount,
                        'unit_price': d_item.selling_price,
                    })
                    i = i + 1
            ctx_whole_dn_details.append({
                'id': delivery_note.id,
                'dn_no': delivery_note.delivery_note_number,
                'lpo_no': delivery_note.lpo_number,
                'project_name': delivery_note.project.name if delivery_note.project else '',
                'sales_items': ctx_item_list,
                'date': delivery_note.date.strftime('%d/%m/%Y') if delivery_note.date else '',
                'customer': delivery_note.customer.customer_name if delivery_note.customer else '',
                'net_total': delivery_note.net_total,
            })
        res = {
            'result': 'ok',
            'delivery_notes': ctx_dn_details,
            'whole_delivery_notes': ctx_whole_dn_details
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=status, mimetype='application/json')

class DNSalesEntry(View):

    def get(self, request, *args, **kwargs):

        current_date = dt.datetime.now().date()

        inv_number = Sales.objects.aggregate(Max('id'))['id__max']

        if not inv_number:
            inv_number = 1
        else:
            inv_number = inv_number + 1
        
        invoice_number = 'INV' + str(inv_number)
        return render(request, 'sales/DN_sales_entry.html',{
            'sales_invoice_number': invoice_number,
            'current_date': current_date.strftime('%d/%m/%Y'),
        })

class DeliveryNoteCreation(View):

    def get(self, request, *args, **kwargs):

        current_date = dt.datetime.now().date()
        prefix = 'DN'
        template_name = ''
        dn_type = request.GET.get('dn_type', '')
        if dn_type == 'inventory_dn':
            template_name = 'sales/inventory_delivery_note.html'
        elif dn_type == 'project_dn':
            template_name = 'sales/project_delivery_note.html'

        ref_number = DeliveryNote.objects.aggregate(Max('id'))['id__max']
        
        if not ref_number:
            ref_number = 1
            
        else:
            ref_number = ref_number + 1
        delivery_no = prefix + str(ref_number)

        context = {
            'current_date': current_date.strftime('%d-%m-%Y'),
            'delivery_no': delivery_no,
        }
        
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):

        dn_dict = ast.literal_eval(request.POST['delivery_note'])
        dn_mode = dn_dict['dn_mode']
        dn, dn_created = DeliveryNote.objects.get_or_create(delivery_note_number=dn_dict['delivery_note_number'])
        if dn_mode == 'project_based':
            project = Project.objects.get(id=int(dn_dict['project_id']))
            dn.project = project
        customer = Customer.objects.get(customer_name=dn_dict['customer'])

        dn.customer = customer
        dn.date = datetime.strptime(dn_dict['date'], '%d-%m-%Y')

        dn.net_total = dn_dict['net_total']
        dn.lpo_number = dn_dict['lpo_no']
        dn.save()

        dn_items = dn_dict['sales_items']
        for item in dn_items:
            itm = Item.objects.get(code=item['item_code'])
            inventory = InventoryItem.objects.get(item=itm)
            d_item, item_created = DeliveryNoteItem.objects.get_or_create(item=itm, delivery_note=dn)
            d_item.quantity_sold = item['qty_sold']
            if dn_dict['dn_mode'] == 'project_based':
                if itm.item_type == 'item':   
                    project_item = ProjectItem.objects.get(item=itm, project=project)
                    if item_created:

                        project_item.quantity = project_item.quantity - int(item['qty_sold'])
                        inventory.quantity = inventory.quantity - int(item['qty_sold'])
                    else:
                        project_item.quantity = int(project_item.quantity) + int(d_item.quantity_sold) - int(item['qty_sold'])      
                        inventory.quantity = int(inventory.quantity) + int(d_item.quantity_sold) - int(item['qty_sold'])      
                    project_item.save()
                    inventory.save()
            else:
                
                if itm.item_type == 'item':
                    if item_created:

                        inventory.quantity = inventory.quantity - int(item['qty_sold'])
                    else:
                        inventory.quantity = int(inventory.quantity) + int(d_item.quantity_sold) - int(item['qty_sold'])      
                inventory.save()
                project_items = ProjectItem.objects.filter(item=itm)
                for pit in project_items:
                    if pit.quantity > inventory.quantity:
                        pit.quantity = inventory.quantity
                        pit.save()
            d_item.quantity_sold = item['qty_sold']
            d_item.net_amount = item['net_amount']
            d_item.selling_price = item['unit_price']
            d_item.save()

        res = {
            'result': 'Ok',
            'id': dn.id,
        }
        response = simplejson.dumps(res)
        status_code = 200
        return HttpResponse(response, status = status_code, mimetype="application/json")

class InventorySales(View):

    def get(self, request, *args, **kwargs):

        current_date = dt.datetime.now().date()

        inv_number = Sales.objects.aggregate(Max('id'))['id__max']

        if not inv_number:
            inv_number = 1
        else:
            inv_number = inv_number + 1
        
        invoice_number = 'INV' + str(inv_number)
        return render(request, 'sales/inventory_sales_entry.html',{
            'sales_invoice_number': invoice_number,
            'current_date': current_date.strftime('%d/%m/%Y'),
        })

class EditSalesInvoice(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'sales/edit_sales_invoice.html', {})

    def post(self, request, *args, **kwargs):

        sales_dict = ast.literal_eval(request.POST['sales'])
        sales = Sales.objects.get(sales_invoice_number=sales_dict['invoice_no'])

        sales.payment_mode = sales_dict['payment_mode']
        
        sales.sales_invoice_date = datetime.strptime(sales_dict['date'], '%d/%m/%Y')
        
        sales.po_no = sales_dict['po_no']
        sales.terms = sales_dict['terms']
        sales.rep = sales_dict['rep']
        sales.via = sales_dict['via']
        sales.fob = sales_dict['fob']

        sales.discount_for_sale = sales_dict['discount_sale']
        sales.discount_percentage_for_sale = sales_dict['discount_percentage']
        sales.round_off = sales_dict['roundoff']
        sales.net_amount = sales_dict['net_total']
        sales.grant_total = sales_dict['grant_total']
        sales.paid = float(sales.paid) + float(sales_dict['paid'])
        customer = Customer.objects.get(customer_name=sales_dict['customer'])
        sales.customer = customer
        if sales_dict['payment_mode'] == 'cheque':
            sales.cheque_no = sales_dict['cheque_no'] 
            sales.bank_name = sales_dict['bank_name']
            sales.bank_branch = sales_dict['branch']
            sales.cheque_date = datetime.strptime(sales_dict['cheque_date'], '%d/%m/%Y')
        if sales_dict['payment_mode'] == 'cheque' or sales_dict['payment_mode'] == 'cash':
            sales.is_processed = True
            sales.paid = sales_dict['grant_total']
        sales.balance = float(sales.grant_total) - float(sales.paid)
        sales.save()

        sales_items = sales_dict['sales_items']
        removed_items = sales_dict['removed_items']

        for r_item in removed_items:
            item = Item.objects.get(code=r_item['item_code'])
            if item.item_type == 'item':
                if sales.project:
                    project_item = ProjectItem.objects.get(item=item, project=sales.project)
                    project_item.quantity = int(project_item.quantity) + int(r_item['qty_sold'])
                    project_item.save()
                inventory = InventoryItem.objects.get(item=item)
                inventory.quantity = int(inventory.quantity) + int(r_item['qty_sold'])
                s_item = SalesItem.objects.get(item=item, sales=sales)
                s_item.delete()

        for item in sales_items:
            item_obj = Item.objects.get(code=item['item_code'])
            s_item = SalesItem.objects.get(item=item_obj, sales=sales)
            if int(s_item.quantity_sold) != int(item['qty_sold']):
                if item_obj.item_type == 'item':
                    if sales.project:
                        project_item = ProjectItem.objects.get(item=item_obj, project=sales.project)
                        project_item.quantity = int(project_item.quantity) + int(s_item.quantity_sold) - int(item['qty_sold'])
                        project_item.save()
                    inventory = InventoryItem.objects.get(item=item_obj)
                    inventory.quantity = int(inventory.quantity) + int(s_item.quantity_sold) - int(item['qty_sold'])
                    inventory.save()
                s_item.quantity_sold = item['qty_sold']
            s_item.net_amount = item['net_amount']
            s_item.selling_price = item['unit_price']
            s_item.save()
        res = {
            'result': 'Ok',
            'id': sales.id,
        }
        response = simplejson.dumps(res)
        status_code = 200
        return HttpResponse(response, status = status_code, mimetype="application/json")

class EditDeliveryNote(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'sales/edit_delivery_note.html', {})

    def post(self, request, *args, **kwargs):
        dn_dict = ast.literal_eval(request.POST['delivery_note'])
        
        dn = DeliveryNote.objects.get(id=dn_dict['id'])
        customer = Customer.objects.get(customer_name=dn_dict['customer'])

        dn.customer = customer
        dn.date = datetime.strptime(dn_dict['date'], '%d/%m/%Y')

        dn.net_total = dn_dict['net_total']
        dn.lpo_number = dn_dict['lpo_no']
        dn.save()

        dn_items = dn_dict['sales_items']
        removed_items = dn_dict['removed_items']
        for r_item in removed_items:
            item = Item.objects.get(code=r_item['item_code'])
            d_item = DeliveryNoteItem.objects.get(item=item, delivery_note=dn)
            if item.item_type == 'item':
                if dn.project:
                    project_item = ProjectItem.objects.get(item=item, project=dn.project)
                    project_item.quantity = int(project_item.quantity) + int(d_item.quantity_sold)
                    project_item.save()
                inventory = InventoryItem.objects.get(item=item)
                inventory.quantity = int(inventory.quantity) + int(d_item.quantity_sold) 
                inventory.save()  
            d_item.delete()  

        for item in dn_items:
            itm = Item.objects.get(code=item['item_code'])
            d_item, item_created = DeliveryNoteItem.objects.get_or_create(item=itm, delivery_note=dn)
            if int(d_item.quantity_sold) != int(item['qty_sold']):
                if itm.item_type == 'item':
                    if dn.project:
                        project_item = ProjectItem.objects.get(item=itm, project=dn.project)
                        if item_created:

                            project_item.quantity = project_item.quantity - int(item['qty_sold'])
                        else:
                            project_item.quantity = int(project_item.quantity) + int(d_item.quantity_sold) - int(item['qty_sold'])      
                        project_item.save()
                    inventory = InventoryItem.objects.get(item=itm)
                    if item_created:
                        inventory.quantity = inventory.quantity - int(item['qty_sold'])
                    else:
                        inventory.quantity = int(inventory.quantity) + int(d_item.quantity_sold) - int(item['qty_sold'])      
                    inventory.save()

            d_item.quantity_sold = item['qty_sold']
            d_item.net_amount = item['net_amount']
            d_item.selling_price = item['unit_price']
            d_item.save()

        res = {
            'result': 'Ok',
            'id': dn.id,
        }
        response = simplejson.dumps(res)
        status_code = 200
        return HttpResponse(response, status = status_code, mimetype="application/json")


class DeliveryNotePDF(View):

    def get(self, request, *args, **kwargs):

        delivery_note_id = kwargs['dn_id']
        delivery_note = DeliveryNote.objects.get(id=delivery_note_id)

        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1300))
        y = 1200
        p = header(p, y)
        p = dn_body_layout(p, y, delivery_note)
        
        y1 = y - 320
        total_amount = 0

        for d_item in delivery_note.deliverynoteitem_set.all():
            
            data=[[Paragraph(d_item.item.name, para_style)]]

            if y1 <= 170:
                y1 = y - 320
                p.showPage()
                p = header(p, y)
                p = dn_body_layout(p, y, delivery_note)

            p.drawString(210, y1, str(d_item.quantity_sold))
            p.drawString(340, y1, str(d_item.item.code))
            # p.drawString(500, y1, str(d_item.item.name))
            table = Table(data, colWidths=[385], rowHeights=100, style=style)      
            table.wrapOn(p, 200, 400)
            table.drawOn(p, 450, y1-10)
            
            y1 = y1 - 50
        
        p = footer(p, y)
        p.showPage()
        p.save()
         
        return response

class SalesInvoicePDF(View):

    def get(self, request, *args, **kwargs):

        invoice_id = kwargs['invoice_id']
        sales = Sales.objects.get(id=invoice_id)

        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1300))
        y = 1200
        p = header(p, y)
        p = invoice_body_layout(p, y, sales)

        total_amount = 0
        y1 = y - 400
        for s_item in sales.salesitem_set.all():
            data=[[Paragraph(s_item.item.name, para_style)]]
                        
            if y1 <= 170:
                y1 = y - 400
                p.showPage()
                p = header(p, y)
                p = invoice_body_layout(p, y, sales)

            p.drawString(60, y1, str(s_item.quantity_sold))
            p.drawString(190, y1, str(s_item.item.code))
            # p.drawString(300, y1, str(item_name))
            table = Table(data, colWidths=[385], rowHeights=100, style=style)      
            table.wrapOn(p, 200, 400)
            table.drawOn(p, 300, y1-10)
            p.drawString(710, y1, str(s_item.selling_price))
            p.drawString(850, y1, str(s_item.net_amount))

            total_amount = total_amount + s_item.net_amount

            y1 = y1 - 50

        #  total box start 
        p.line(50, y - 1020, 950, y - 1020)
        p.line(650, y - 980, 650, y - 1020)
        p.line(50, y - 980, 50, y - 1020)
        p.line(950, y - 980, 950, y - 1020)

        # total box end
        p.drawString(820, y - 1010, 'DHS')
        p.drawString(850, y - 1010, str(total_amount))

        p.setFont("Helvetica-Bold", 30)  
        p.drawString(660, y - 1010, 'Total')
        p = footer(p, y)

        # Item Box end

        p.showPage()
        p.save()
         
        return response

class PrintDeliveryNotes(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'sales/print_delivery_note.html', {})

class PrintSalesInvoice(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'sales/print_invoice.html', {})

class CheckDeliverynoteExistence(View):

    def get(self, request, *args, **kwargs):

        delivery_no = request.GET.get('delivery_no', '')
        try:
            delivery_note = DeliveryNote.objects.get(delivery_note_number=delivery_no)
            res = {
                'result': 'error',
            }
        except Exception as ex:

            res = {
                'result': 'ok',
            }

        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')

class CheckInvoiceExistence(View):

    def get(self, request, *args, **kwargs):

        invoice_no = request.GET.get('invoice_no', '')
        try:
            invoice = Sales.objects.get(sales_invoice_number=invoice_no)
            res = {
                'result': 'error',
            }
        except Exception as ex:

            res = {
                'result': 'ok',
            }

        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')


class CheckReceiptVoucherExistence(View):

    def get(self, request, *args, **kwargs):

        rv_no = request.GET.get('rv_no', '')
        try:
            receiptvoucher = ReceiptVoucher.objects.get(receipt_voucher_no=rv_no)
            res = {
                'result': 'error',
            }
        except Exception as ex:

            res = {
                'result': 'ok',
            }

        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')
