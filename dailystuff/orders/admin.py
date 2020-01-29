from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import OrderItem, Order
from .order_analytics import get_orders_product_details
from .order_analytics import get_orders_product_customer_details
from .order_analytics import order_product_summary


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    fieldsets = [
        ('Product', {'fields': ['product'],}),
        ('Quantity', {'fields': ['quantity'],}),
        ('Price', {'fields': ['price'],}),
    ]
    readonly_fields = ['product', 'quantity', 'price']
    can_delete = False
    max_num = 0
    template = 'admin/orders/tabular.html'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    actions = ['get_orders_detail', 'get_orders_customer_detail', 'get_orders_product_analysis']
    list_display = ['id', 'billingName', 'email_id', 'created_at','customerId', 'total']
    list_display_links = ('id', 'billingName')
    search_fields = ['id', 'billingName', 'email_id']
    readonly_fields = ['id', 'token', 'total', 'email_id', 'created_at', 'billingName', 'billingAddress1',
                       'billingCity', 'billingPostcode', 'billingCountry', 'shippingName', 'shippingAddress1',
                       'shippingCity', 'shippingPostcode', 'shippingCountry']
    fieldsets = [
        ('ORDER INFORMATION', {'fields': ['id', 'token', 'total', 'created_at']}),
        ('BILLING INFORMATION', {'fields': ['billingName', 'billingAddress1', 'billingCity',
                                            'billingPostcode', 'billingCountry', 'email_id']}),
        ('SHIPPING INFORMATION', {'fields': ['shippingName', 'shippingAddress1', 'shippingCity',
                                             'shippingPostcode', 'shippingCountry']}),
    ]

    inlines = [
        OrderItemAdmin,
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_orders_detail(self, request, queryset):
        column_names = ['Order ID', 'Product Name', 'Price', 'Quantity']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format("orders_productlist")
        writer = csv.writer(response)
        writer.writerow(column_names)
        result = get_orders_product_details()
        for order_item in result:
            writer.writerow(order_item)
        return response

    def get_orders_customer_detail(self, request, queryset):
        column_names = ['Order ID', 'Product Name', 'Price', 'Quantity',
                        'Customer ID', 'Email', 'First Name', 'Last Name']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format("orders_customerlist")
        writer = csv.writer(response)
        writer.writerow(column_names)
        result = get_orders_product_customer_details()
        for order_item in result:
            writer.writerow(order_item)
        return response

    def get_orders_product_analysis(self, request, queryset):
        column_names = ['Minimun Order', 'Maximum Order', 'Total OrderValue', 'Total Service Value']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format("orders_product_summary")
        writer = csv.writer(response)
        writer.writerow(column_names)
        result = order_product_summary()
        writer.writerow(result)
        return response
