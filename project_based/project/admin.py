from django.contrib import admin
from project.models import *

class InventoryItemAdmin(admin.ModelAdmin):
	readonly_fields = ('quantity', )

class ProjectItemAdmin(admin.ModelAdmin):
	readonly_fields = ('quantity', )

# admin.site.register(Project)
# admin.site.register(Item)
admin.site.register(ProjectItem, ProjectItemAdmin)
admin.site.register(InventoryItem, InventoryItemAdmin)

