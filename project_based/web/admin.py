from django.contrib import admin
from web.models import *

class CashInHandAdmin(admin.ModelAdmin):
	readonly_fields = ('amount', )

admin.site.register(CashInHand, CashInHandAdmin)


# admin.site.register(Supplier)
# admin.site.register(Customer)
# admin.site.register(TransportationCompany)
# admin.site.register(OwnerCompany)
# admin.site.register(CashEntry)



