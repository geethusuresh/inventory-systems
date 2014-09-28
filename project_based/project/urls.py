
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from project.views import *

urlpatterns = patterns('',
	url(r'create_project/$', login_required(CreateProject.as_view()), name='create_project'),
	url(r'delete_project/$', login_required(DeleteProject.as_view()), name='delete_project'),
	url(r'projects/$', login_required(Projects.as_view()), name='projects'),
	url(r'add_item/$', login_required(AddItem.as_view()), name='add_item'),
	url(r'edit_item/(?P<item_id>\d+)/$', login_required(EditItem.as_view()), name='edit_item'),
	url(r'project_items/$', login_required(ProjectItemList.as_view()), name='project_items'),
	url(r'items/$', login_required(ItemList.as_view()), name='items'),
	url(r'service_charges/$', login_required(ServiceChargeList.as_view()), name='service_charges'),
)