
import sys
import ast
import simplejson
import datetime as dt
from datetime import datetime
from decimal import *
import math
import os

from django.db import IntegrityError
from django.db.models import Max
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings

from sales.models import *
from project.models import *
from web.models import *
from .models import *


class AddExpenseHead(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'expenses/add_expense_head.html', {})

    def post(self, request, *args, **kwargs):

        post_dict = request.POST
        status = 200

        try:
            if len(post_dict['head_name']) > 0 and not post_dict['head_name'].isspace():
                expense_head, created = ExpenseHead.objects.get_or_create(expense_head = post_dict['head_name'])
                if created:
                    context = {
                        'message' : 'Added successfully',
                    }
                    res = {
                        'result': 'ok',
                        'head_id': expense_head.id,
                    }
                else:
                    context = {
                        'message' : 'This Head name is Already Existing',
                    }
                    res = {
                        'result': 'error',
                        'message': 'This Head name is Already Existing',
                    }

            else:
                context = {
                    'message' : 'Head name Cannot be null',
                }
        except Exception as ex:
            context = {
                'message' : post_dict['head_name']+' is already existing',
            }
            res = {
                'result': 'error',
                'message': post_dict['head_name']+' is already existing',
            }
        if request.is_ajax():
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
        return render(request, 'expenses/add_expense_head.html', context)

class ExpenseHeadList(View):

    def get(self, request, *args, **kwargs):

        ctx_expense_head = []
        status_code = 200
        expense_heads = ExpenseHead.objects.all()
        if len(expense_heads) > 0:
            for head in expense_heads:
                ctx_expense_head.append({
                    'head_name': head.expense_head,
                    'id': head.id, 
                })
        res = {
            'result': 'ok',
            'expense_heads':ctx_expense_head
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=status_code, mimetype="application/json")

class ExpenseList(View):

    def get(self, request, *args, **kwargs):
        expenses = Expense.objects.all()

        if request.is_ajax():
            ctx_expense_head = []
            status_code = 200
            if len(expenses) > 0:
                for expense in expenses:
                    ctx_expense_head.append({
                        'head_name': expense.expense_head,
                        'id': expense.id, 
                        'date': expense.date.strftime('%d/%m/%Y'),
                        'voucher_no': expense.voucher_no,
                        'amount': expense.amount
                    })
            res = {
                'result': 'ok',
                'expenses': expenses
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status_code, mimetype="application/json")
        return render(request, 'expenses/expense_list.html', {'expenses': expenses})

class EditExpense(View):

    def get(self, request, *args, **kwargs):
        expense = Expense.objects.get(id=request.GET['expense_id'])

        try:
            cash_in_hand = CashInHand.objects.latest('id')
        except:
            cash_in_hand = None
        
        if request.is_ajax():
            ctx_expense = []
            status_code = 200
            if expense:
                ctx_expense.append({
                    'expense_head_id': expense.expense_head.id if expense.expense_head else '',
                    'id': expense.id, 
                    'date': expense.date.strftime('%d/%m/%Y'),
                    'voucher_no': expense.voucher_no,
                    'amount': expense.amount,
                    'project_id': expense.project.id if expense.project else '',
                    'payment_mode': expense.payment_mode,
                    'branch': expense.branch,
                    'bank_name': expense.bank_name,
                    'cheque_no': expense.cheque_no,
                    'cheque_date': expense.cheque_date.strftime('%d/%m/%Y') if expense.cheque_date else '',
                    'narration': expense.narration,
                })
            res = {
                'result': 'ok',
                'expense': ctx_expense
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status_code, mimetype="application/json")
        return render(request, 'expenses/edit_expense.html', {'expense': expense, 'cash_in_hand': cash_in_hand.amount if cash_in_hand else 0,})
    
    def post(self, request, *args, **kwargs):

        expense_details = ast.literal_eval(request.POST['expense'])
        status = 200
        try:
            cash_in_hand = CashInHand.objects.latest('id')
        except:
            cash_in_hand = None
        expense = Expense.objects.get(id=expense_details['id'])
        try:
            expense.voucher_no = expense_details['voucher_no']
            expense.date = datetime.strptime(expense_details['date'], '%d/%m/%Y')
            expense.payment_mode = expense_details['payment_mode']
            expense.narration = expense_details['narration']
            expense.cheque_no = expense_details['cheque_no']
            if expense_details['cheque_date']:
                expense.cheque_date = datetime.strptime(expense_details['cheque_date'], '%d/%m/%Y')
            expense.bank_name = expense_details['bank_name']
            expense.branch = expense_details['branch']
            expense_head = ExpenseHead.objects.get(id=expense_details['expense_head_id'])
            expense.expense_head = expense_head
            
            if expense.project:
                project = expense.project
                project.expense_amount = float(project.expense_amount) - float(expense.amount)
                project.save()
            if expense_details['project_id']:
                project = Project.objects.get(id=expense_details['project_id'])
                project.expense_amount = float(project.expense_amount) + float(expense_details['amount'])
                project.save()
                expense.project = project
            cash_in_hand.amount = float(cash_in_hand.amount) + float(expense.amount)
            expense.amount = expense_details['amount']
            cash_in_hand.amount = float(cash_in_hand.amount) - float(expense_details['amount'])
            cash_in_hand.save()
            expense.save()
            if expense.purchase:
                purchase = expense.purchase
                purchase.purchase_expense = expense_details['amount']
                purchase.save()
            res = {
                'result': 'ok',
            }
        except Exception as ex:
            print str(ex)
            res = {
                'result': 'error',
                'message': 'Voucher No already existing'
            }
        response = simplejson.dumps(res)

        return HttpResponse(response, status=status, mimetype='application/json')

class Expenses(View):

    def get(self, request, *args, **kwargs):

        current_date = dt.datetime.now().date()
        expenses = Expense.objects.all().count()
        try:
            cash_in_hand = CashInHand.objects.latest('id')
        except:
            cash_in_hand = None

        if int(expenses) > 0:
            latest_expense = Expense.objects.latest('id')
            voucher_no = int(latest_expense.voucher_no) + 1
        else:
            voucher_no = 1
        context = {
            'current_date': current_date.strftime('%d/%m/%Y'),
            'voucher_no': voucher_no,
            'cash_in_hand': cash_in_hand.amount if cash_in_hand else 0,
        }
        
        return render(request, 'expenses/expense.html', context)

    def post(self, request, *args, **kwargs):

        post_dict = ast.literal_eval(request.POST['expense'])
        try:
            expense = Expense.objects.get(voucher_no=post_dict['voucher_no'])
            res = {
                'result': 'error',
                'message': 'Voucher No already Existing'
            }
        except Exception as ex:
            print str(ex)
            expense = Expense.objects.create(created_by=request.user, voucher_no=post_dict['voucher_no'])
            expense.expense_head = ExpenseHead.objects.get(id = post_dict['expense_head_id'])
            expense.date = datetime.strptime(post_dict['date'], '%d/%m/%Y')
            expense.amount = post_dict['amount']
            expense.payment_mode = post_dict['payment_mode']
            expense.narration = post_dict['narration']
            try:
                cash_in_hand = CashInHand.objects.latest('id')
            except Exception as ex:
                cash_in_hand = None
            if cash_in_hand:
                cash_in_hand.amount = float(cash_in_hand.amount) - float(post_dict['amount'])
                cash_in_hand.save()
                cash_entry = CashEntry.objects.create(cash_in_hand=cash_in_hand)
                cash_entry.in_out = 'out'
                cash_entry.date = datetime.strptime(post_dict['date'], '%d/%m/%Y')
                cash_entry.from_to = 'Expense'
                cash_entry.amount = post_dict['amount']
            if post_dict['payment_mode'] == 'cheque':
                expense.cheque_no = post_dict['cheque_no']
                expense.cheque_date = datetime.strptime(post_dict['cheque_date'], '%d/%m/%Y')
                expense.bank_name = post_dict['bank_name']
                expense.branch = post_dict['branch']
            expense.save()
            try:
                project = Project.objects.get(id=post_dict['project_id'])
                project.expense_amount = float(project.expense_amount) + float(post_dict['amount'])
                cash_entry.purpose = 'other'
                cash_entry.other_purpose = post_dict['narration']
                cash_entry.project = project
                project.save()
                expense.project = project
                expense.save()
            except Exception as ex:
                cash_entry.purpose = 'other'
                cash_entry.other_purpose = post_dict['narration']
                print str(ex)
                project = None
            cash_entry.save()
            res = {
                'result': 'ok'
            }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype="application/json")