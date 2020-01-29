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
