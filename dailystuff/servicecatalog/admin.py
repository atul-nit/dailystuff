from django.contrib import admin
from .models import ServiceCategory, ServiceProduct


class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name', 'url_key']
    list_display_links = ['id', 'category_name']
    prepopulated_fields = {'url_key': ('category_name',)}
    ordering = ['id']

class ServiceProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'url_key', 'stock']
    list_display_links = ['id', 'product_name']
    prepopulated_fields = {'url_key': ('product_name',)}
    list_editable = ['stock']
    ordering = ['id']

admin.site.register(ServiceCategory, ServiceCategoryAdmin)
admin.site.register(ServiceProduct, ServiceProductAdmin)