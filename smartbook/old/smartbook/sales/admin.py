from django.contrib import admin
from sales.models import *

admin.site.register(Sales)
admin.site.register(SalesItem)
admin.site.register(SalesReturn)
admin.site.register(SalesReturnItem)