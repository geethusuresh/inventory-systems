import simplejson
import re
import ast
from datetime import datetime

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from web.models import (Supplier, Customer, TransportationCompany, CashInHand, CashEntry)

class Home(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'home.html',context)

class Login(View):

    def post(self, request, *args, **kwargs):

        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user and user.is_active:
            login(request, user)
        else:
            context = {
                'message' : 'Username or password is incorrect'
            }
            return render(request, 'home.html',context)
        return HttpResponseRedirect(reverse('home'))

class Logout(View):

    def get(self, request, *args, **kwargs):

        logout(request)
        return HttpResponseRedirect(reverse('home'))

class UserList(View):
    def get(self, request, *args, **kwargs):
        user_type = kwargs['user_type']
        ctx_suppliers = []
        ctx_customers = []
        ctx_salesman = []
        users = []
        if user_type == 'supplier':
            users = Supplier.objects.all()
            if request.is_ajax():
                if len(users) > 0:
                    for usr in users:
                        ctx_suppliers.append({
                            'supplier_name': usr.name,
                        })
                res = {
                    'suppliers': ctx_suppliers,
                    
                } 
                
                response = simplejson.dumps(res)
                status_code = 200
                return HttpResponse(response, status = status_code, mimetype="application/json")

        elif user_type == 'customer':
            users = Customer.objects.all()
            
            if request.is_ajax():
                if len(users) > 0:
                    for customer in users:
                        ctx_customers.append({
                            'customer_name': customer.customer_name,
                            'id': customer.id,
                        })
                res = {
                    'customers': ctx_customers,                    
                } 
                response = simplejson.dumps(res)
                status_code = 200
                return HttpResponse(response, status = status_code, mimetype="application/json")

        return render(request, 'user_list.html',{
            'users': users,
            'user_type': user_type
        })


class RegisterUser(View):
    def get(self, request, *args, **kwargs):
        user_type = kwargs['user_type']
        print user_type
        return render(request, 'register_user.html',{'user_type': user_type})
        

    def post(self, request, *args, **kwargs):
       
        context={}
        user_type = kwargs['user_type']
        message = ''
        template = 'register_user.html'
        email_validation = (re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", request.POST['email']) )
        if not request.is_ajax():
            if request.POST['name'] == '':
                message = "Please enter Name"
            elif request.POST['email'] == '' and user_type != 'supplier':
                message = "Please enter email"
            elif email_validation == None and user_type != 'supplier':
                message = "Please enter a valid email id"
            elif user_type == "supplier":
                if request.POST['contact_person'] == '':
                    message = "Please enter Contact Person"
                elif request.POST['mobile'] == '':
                    message = "Please enter Mobile Number"
                if request.POST['mobile'] != '':
                    if len(request.POST['mobile']) > 15:
                        message = 'Please enter a valid mobile no.'
                if request.POST['phone'] != '':
                    if len(request.POST['phone']) > 15:
                        message = 'Please enter a valid phone no.'

        if message:
            context = {
                'error_message': message,
                'user_type': user_type
            }
            context.update(request.POST)            
            return render(request, template, context)
        else:
            if user_type == 'supplier':
                try:
                    supplier = Supplier()
                    supplier.email_id = request.POST['email']
                    supplier.name = request.POST['name']
                    supplier.user_type = 'supplier'
                    supplier.house_name = request.POST['house']
                    supplier.street = request.POST['street']
                    supplier.city = request.POST['city']
                    supplier.district = request.POST['district']
                    supplier.pin = request.POST['pin']
                    supplier.mobile = request.POST['mobile']
                    supplier.land_line = request.POST['phone']
                    supplier.contact_person = request.POST['contact_person']
                    supplier.save()
                    if request.is_ajax():
                        res = {
                            'result': 'ok',
                            'supplier_name': supplier.name
                        }
                        response = simplejson.dumps(res)
                        return HttpResponse(response, status = 200, mimetype="application/json")
                except IntegrityError as e:
                    print "es:", type(e)
                    if request.is_ajax():
                        res = {
                            'result': 'error',
                            'error_message': "Supplier with this name already exists"
                        }
                        response = simplejson.dumps(res)
                        return HttpResponse(response, status = 200, mimetype="application/json")
                    else:
                        context = {
                            'error_message': "Supplier with this name already exists",
                            'user_type': user_type
                        }
                        context.update(request.POST)            
                        return render(request, template, context)

                users = Supplier.objects.all()
                return render(request, 'user_list.html',{
                    'users': users,
                    'user_type': user_type
                })

            return render(request, 'register_user.html',context)

class EditUser(View):

    def get(self, request, *args, **kwargs):

        user_type = kwargs['user_type']
        if user_type == 'customer':
            userprofile = Customer.objects.get(id=kwargs['user_id'])
        else:
            userprofile = Supplier.objects.get(id=kwargs['user_id'])
        return render(request, 'edit_user.html',{'user_type': user_type, 'profile': userprofile})

    def post(self, request, *args, **kwargs):

        user_type = kwargs['user_type']
        post_dict = request.POST
        email_validation = (re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", request.POST['email']) )
        if user_type == 'customer':
            profile = customer = Customer.objects.get(id = kwargs['user_id'])
        elif user_type == 'supplier':
            profile = supplier = Supplier.objects.get(id = kwargs['user_id'])
        if request.POST['name'] == '':
            context = {
                'message': 'Name cannot be null',
                'user_type': user_type,
                'profile': profile
            }
            context.update(request.POST)
            return render(request, 'edit_user.html',context)
        elif request.POST['email'] == '':
            context = {
                'message': 'Email cannot be null',
                'user_type': user_type,
                'profile': profile
            }
            context.update(request.POST)
            return render(request, 'edit_user.html',context)
        if email_validation == None:
            message = "Please enter a valid email id"
            context = {
                'message': message,
                'user_type': user_type,
                'profile': profile
            }
            context.update(request.POST)
            return render(request, 'edit_user.html',context)  

        if user_type == 'customer':
            customer.customer_name = request.POST['name']
            customer.house_name =request.POST['house']
            customer.street = request.POST['street']
            customer.city = request.POST['city']
            customer.district = request.POST['district']
            customer.pin = request.POST['pin']
            customer.mobile_number = request.POST['mobile']
            customer.land_line = request.POST['phone']
            customer.customer_id = request.POST['email']
            customer.save()
            context = {
                'message' : 'Customer edited correctly',
                'user_type': user_type,
                'profile': customer
            }
            return render(request, 'edit_user.html',context)
        else:   
            supplier.user_type=user_type
            supplier.name = request.POST['name']
            supplier.house_name =request.POST['house']
            supplier.street = request.POST['street']
            supplier.city = request.POST['city']
            supplier.district = request.POST['district']
            supplier.pin = request.POST['pin']
            supplier.mobile = request.POST['mobile']
            supplier.land_line = request.POST['phone']
            supplier.email_id = request.POST['email']
            supplier.contact_person= request.POST['contact_person']
            supplier.save()
            if user_type == 'supplier':
            
                context = {
                    'message' : 'Supplier edited correctly',
                    'user_type': user_type,
                    'profile': supplier
                }
                return render(request, 'edit_user.html',context)

class DeleteUser(View):

    def get(self, request, *args, **kwargs):

        user_type = kwargs['user_type']
        if request.user.is_superuser:
            if user_type == 'customer':
                customer = Customer.objects.get(id=kwargs['user_id'])
                customer.delete()
            else:
                supplier = Supplier.objects.get(id=kwargs['user_id'])            
                supplier.delete()
                context = {
                    'message': 'Deleted Successfully'
                }
        else:
            context = {
                'message': "You don't have permission to perform this action"
            }
        return HttpResponseRedirect(reverse('users', kwargs={'user_type': user_type}))

class CreateCustomer(View):

    def get(self, request, *args, **kwargs):

        user_type = 'customer'
        return render(request, 'register_user.html',{'user_type': user_type})

    def post(self, request, *args, **kwargs):

        if not request.is_ajax():
            email_validation = (re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", request.POST['email']) )
            if request.POST['name'] == '':
                context = {
                    'error_message': 'Please enter the name',
                    'user_type': 'customer',
                }
                context.update(request.POST)
                return render(request, 'register_user.html',context)
            
            elif request.POST['mobile'] != '':
                if len(request.POST['mobile']) > 15:
                    context = {
                        'error_message': 'Please enter a valid mobile no',
                        'user_type': 'customer',
                    }
                    context.update(request.POST)
                    return render(request, 'register_user.html',context)
            elif request.POST['phone'] != '':
                if len(request.POST['phone']) > 15:
                    context = {
                        'error_message': 'Please enter a valid phone no.',
                        'user_type': 'customer',
                    }
                    context.update(request.POST)
                    return render(request, 'register_user.html',context)
        try:
            customer = Customer.objects.get(customer_name = request.POST['name'])
            if request.is_ajax():
                res = {
                    'result': 'error',
                    'message': 'Customer with this name already exists',
                }
                response = simplejson.dumps(res)
                return HttpResponse(response, status = 200, mimetype="application/json")
            else:
                context = {
                    'error_message': 'Customer with this name already exists',
                    'user_type': 'customer',
                }
                context.update(request.POST)
                return render(request, 'register_user.html',context)
        except Exception as ex:
            customer = Customer.objects.create(customer_name = request.POST['name'])
            customer.customer_name = request.POST['name']
            customer.user_type = 'customer'
            customer.house_name = request.POST['house'] 
            customer.street = request.POST['street']
            customer.city = request.POST['city']
            customer.district = request.POST['district'] 
            customer.pin = request.POST['pin']
            customer.mobile_number = request.POST['mobile']
            customer.land_line = request.POST['phone']
            customer.customer_id = request.POST['email']
            customer.save()
            if request.is_ajax():
                res = {
                    'result': 'ok',
                    'customer_name': customer.customer_name
                }
                response = simplejson.dumps(res)
                return HttpResponse(response, status = 200, mimetype="application/json")
            users = Customer.objects.all()
            return render(request, 'user_list.html',{
                'users': users,
                'user_type': 'customer'
            })

class TransportationCompanyList(View):

    def get(self, request, *args, **kwargs):

        ctx = []
        transportationcompanies = TransportationCompany.objects.all()
        if len(transportationcompanies) > 0:
            for transportationcompany in transportationcompanies:
                ctx.append({
                    'company_name': transportationcompany.company_name,    
                })
        res = {
            'company_names': ctx,    
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype="application/json")

class AddTransportationCompany(View):

    def post(self, request, *args, **kwargs):

        if len(request.POST['new_company']) > 0 and not request.POST['new_company'].isspace():
            new_company, created = TransportationCompany.objects.get_or_create(company_name=request.POST['new_company']) 
            if not created:
                res = {
                    'result': 'error',
                    'message': 'Company name already exists'
                }
            else:
                res = {
                    'result': 'ok',
                    'company_name': new_company.company_name
                }
        else:
            res = {
                 'result': 'error',
                 'message': 'Company name cannot be null'
            }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')
from project.models import Project

class CreateCashEntry(View):

    def get(self, request, *args, **kwargs):
        current_date = datetime.now()
        context = {
            'date': current_date.strftime('%d/%m/%Y')
        }
        return render(request, 'cash_entry.html', context)

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            status = 200
            cash_entry_details = ast.literal_eval(request.POST['cash_entry'])
            try:
                cash_in_hand = CashInHand.objects.latest('id')
            except Exception as ex:
                cash_in_hand = CashInHand()
            cash_in_hand.amount = float(cash_in_hand.amount) + float(cash_entry_details['amount'])
            cash_in_hand.save()
            cash_entry = CashEntry.objects.create(cash_in_hand=cash_in_hand)
            cash_entry.in_out = 'in'
            cash_entry.date = datetime.strptime(cash_entry_details['date'], '%d/%m/%Y')
            cash_entry.from_to = cash_entry_details['from']
            cash_entry.amount = cash_entry_details['amount']
            cash_entry.purpose = cash_entry_details['purpose']
            if cash_entry_details['purpose'] == 'project':
                try:
                    project = Project.objects.get(id=cash_entry_details['project_id'])
                    cash_entry.project = project
                    project.budget_amount = float(project.budget_amount) + float(cash_entry_details['amount'])
                    project.save()
                except Exception as ex:
                    project = None
            elif cash_entry_details['purpose'] == 'other':
                cash_entry.other_purpose = cash_entry_details['other_purpose']
            cash_entry.save()
            res = {
                'result': 'ok',
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')