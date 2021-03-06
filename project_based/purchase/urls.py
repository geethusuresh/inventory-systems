from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from purchase.views import *

urlpatterns = patterns('',
	url(r'^entry/$', login_required(PurchaseEntry.as_view()), name='purchase'),
	url(r'^purchase_details/$', login_required(PurchaseDetails.as_view()), name='purchase_details'),
)