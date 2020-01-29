from django.db import connection

def get_orders_product_details():
    result = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT o.id, oi.product, oi.price, oi.quantity '
                       'FROM Orders as o INNER JOIN OrderItem as oi ON o.id=oi.order_id ')
        for order in cursor:
            result.append(order)
    return result

def get_orders_product_customer_details():
    result = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT o.id, oi.product, oi.price, oi.quantity, user.id, '
                       'user.email, user.first_name, user.last_name '
                       'FROM Orders as o INNER JOIN OrderItem as oi ON o.id=oi.order_id '
                       'INNER JOIN auth_user as user on o.customerId=user.id')
        for order in cursor:
            result.append(order)
    return result

def get_minimum_order():
    min_order = 0
    with connection.cursor() as cursor:
        cursor.execute('SELECT min(total) FROM Orders')
        for r in cursor:
            min_order = r[0]
    return min_order

def get_maximum_order():
    max_order = 0
    with connection.cursor() as cursor:
        cursor.execute('SELECT max(total) FROM Orders')
        for r in cursor:
            max_order = r[0]
    return max_order

def get_total_order_value():
    total_order = 0
    with connection.cursor() as cursor:
        cursor.execute('SELECT sum(total) FROM Orders')
        for r in cursor:
            total_order = r[0]
    return total_order

def get_total_service_value():
    total_service_value = 0
    with connection.cursor() as cursor:
        cursor.execute('SELECT sum(service_cost) FROM servicecatalog_serviceproduct')
        for r in cursor:
            total_service_value = r[0]
    return total_service_value

def order_product_summary():
    result = []
    result.append(get_minimum_order())
    result.append(get_maximum_order())
    result.append(get_total_order_value())
    result.append(get_total_service_value())
    return result

