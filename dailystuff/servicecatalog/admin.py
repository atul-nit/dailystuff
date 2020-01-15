from django.contrib import admin
from .models import ServiceCategory, ServiceProduct
from .product_analytics import get_product_list_name
from .product_analytics import get_all_products
from .product_analytics import get_all_active_products


class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name', 'url_key']
    list_display_links = ['id', 'category_name']
    prepopulated_fields = {'url_key': ('category_name',)}
    ordering = ['id']

class ServiceProductAdmin(admin.ModelAdmin):
    actions = ['get_products_list', 'get_all_products', 'get_all_active_products']
    list_display = ['id', 'product_name', 'url_key', 'stock']
    list_display_links = ['id', 'product_name']
    prepopulated_fields = {'url_key': ('product_name',)}
    list_editable = ['stock']
    ordering = ['id']

    def get_products_list(self, request, queryset):
        get_product_list_name()

    def get_all_products(self, request, queryset):
        get_all_products()

    def get_all_active_products(self, request, queryset):
        get_all_active_products()

admin.site.register(ServiceCategory, ServiceCategoryAdmin)
admin.site.register(ServiceProduct, ServiceProductAdmin)