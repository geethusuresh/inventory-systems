import sys
import simplejson

from django.db import IntegrityError

from django.contrib.auth.views import password_reset
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from inventory.models import Item, Inventory
from inventory.models import UnitOfMeasure
from inventory.models import Brand

class ItemAdd(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'inventory/new_item.html',{})

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            try:
                uom = UnitOfMeasure.objects.get(uom = request.POST['uom'])
                brand = Brand.objects.get(brand = request.POST['brand'])
                item, created = Item.objects.get_or_create(code=request.POST['code'], brand=brand, uom=uom)
                if not created:
                    res = {
                        'result': 'error',
                        'message': 'Item with this item code already existing'
                    }
                    status_code = 500
                else:
                    item.name=request.POST['name']
                    item.description=request.POST['description']
                    item.barcode=request.POST['barcode']
                    item.tax=request.POST['tax']
                    item.save()
                    res = {
                        'result': 'ok',
                    }  
                    status_code = 200 
                
            except IntegrityError:
                res = {
                        'result': 'error',
                        'message': 'Item with this item code already existing'
                    }
                status_code = 500

            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")


class ItemList(View):
    
    def get(self, request, *args, **kwargs):
        
            if request.is_ajax():
                try:
                    item_code = request.GET.get('item_code', '')
                    item_name = request.GET.get('item_name', '')
                    barcode = request.GET.get('barcode', '')
                    items = []
                    if item_code:
                        items = Item.objects.filter(code__istartswith=item_code)
                    elif item_name:
                        items = Item.objects.filter(name__istartswith=item_name)
                    elif barcode:
                        items = Item.objects.filter(barcode__istartswith=barcode)
                    item_list = []
                    for item in items:
                        item_list.append({
                            'item_code': item.code,
                            'item_name': item.name,
                            'barcode': item.barcode,
                            'brand': item.brand.brand,
                            'tax': item.tax,
                            'uom': item.uom.uom,
                            'current_stock': item.inventory_set.all()[0].quantity if item.inventory_set.count() > 0  else 0 ,
                            'selling_price': item.inventory_set.all()[0].selling_price if item.inventory_set.count() > 0 else 0 ,
                            'discount_permit': item.inventory_set.all()[0].discount_permit_amount if item.inventory_set.count() > 0 else 0,
                        })

                    res = {
                        'items': item_list,
                    }
                    response = simplejson.dumps(res)

                except Exception as ex:
                    response = simplejson.dumps({'result': 'error', 'error': str(ex)})
                    status_code = 500
                status_code = 200
                return HttpResponse(response, status = status_code, mimetype = 'application/json')
            else:
                inventory = Inventory.objects.all()
                ctx = {
                    'inventory': inventory
                }
                return render(request, 'inventory/stock.html',ctx)

class BrandList(View):

    def get(self, request, *args, **kwargs):

        ctx_brand = []
        brands = Brand.objects.all()
        if len(brands) > 0:
            for brand in brands:
                ctx_brand.append({
                    'brand_name': brand.brand,
                })
        res = {
            'brands': ctx_brand,
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status = 200, mimetype="application/json")

class AddBrand(View):

    def post(self, request, *args, **kwargs):

        if len(request.POST['brand_name']) > 0 and not request.POST['brand_name'].isspace():
            brand, created = Brand.objects.get_or_create(brand=request.POST['brand_name']) 
            if not created:
                res = {
                    'result': 'error',
                    'message': 'Brand name Already exists'
                }
            else:
                res = {
                    'result': 'ok',
                    'brand': brand.brand
                }
        else:
            res = {
                 'result': 'error',
                 'message': 'Brand name Cannot be null'
            }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')

class UomList(View):

    def get(self, request, *args, **kwargs):

        ctx_uom = []
        uoms = UnitOfMeasure.objects.all()
        if len(uoms) > 0:
            for uom in uoms:
                ctx_uom.append({
                    'uom_name': uom.uom,
                })
        res = {
            'uoms': ctx_uom,
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status = 200, mimetype="application/json")

class AddUom(View):

    def post(self, request, *args, **kwargs):

        if len(request.POST['uom_name']) > 0 and not request.POST['uom_name'].isspace():
            uom, created = UnitOfMeasure.objects.get_or_create(uom=request.POST['uom_name']) 
            if not created:
                res = {
                    'result': 'error',
                    'message': 'Uom Already exists'
                }
            else:
                res = {
                    'result': 'ok',
                    'brand': uom.uom
                }
        else:
            res = {
                 'result': 'error',
                 'message': 'Uom Cannot be null'
            }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')



