from django.contrib import admin
from django.http import HttpResponse
import csv
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
    list_display = ['id', 'product_name', 'url_key', 'stock', 'is_available']
    list_display_links = ['id', 'product_name']
    prepopulated_fields = {'url_key': ('product_name',)}
    list_editable = ['stock']
    ordering = ['id']

    def get_products_list(self, request, queryset):
        column_names = ["ID", "Service Name", 'Availability']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format("productslist")
        writer = csv.writer(response)
        writer.writerow(column_names)
        result = get_product_list_name()
        try:
            if result['actions_completed']:
                products_list = result['result']
                for item in products_list:
                    writer.writerow(item)
            else:
                raise Exception("All Actions not completed")
        except Exception as e:
            print(e)
        return response

    def get_all_active_products(self, request, queryset):
        column_names = ["ID", "Service Name"]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format("active_productslist")
        writer = csv.writer(response)
        writer.writerow(column_names)
        result = get_all_active_products()
        try:
            if result['actions_completed']:
                products_list = result['result']
                for item in products_list:
                    writer.writerow(item)
            else:
                raise Exception("All Actions not completed")
        except Exception as e:
            print(e)
        return response

admin.site.register(ServiceCategory, ServiceCategoryAdmin)
admin.site.register(ServiceProduct, ServiceProductAdmin)