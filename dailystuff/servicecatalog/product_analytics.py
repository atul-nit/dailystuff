from django.db import connection

def get_product_list_name():
    result = []
    with connection.cursor() as cursor:
        # cursor.execute("SELECT id, product_name FROM servicecatalog_serviceproduct where id=:Id", {"Id": 3})
        t = (2, )
        cursor.execute('SELECT id, product_name FROM servicecatalog_serviceproduct where id in (:id)', {'id': "3,2"})
        for product in cursor:
            result.append(product)
    print(result)

def get_all_active_products():
    result = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT id, product_name FROM servicecatalog_serviceproduct where is_available=:active', {'active': 1})
        for product in cursor:
            result.append(product)
    print(result)

def get_all_ids():
    all_ids = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT id from servicecatalog_serviceproduct')
        for row in cursor:
            all_ids.append(row[0])
    return all_ids

def get_all_products():
    result = []
    product_ids = get_all_ids()
    id_str = ', '.join(str(id) for id in product_ids)
    print(id_str)
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, product_name FROM servicecatalog_serviceproduct where id in (?)", (id_str,))
        for product in cursor:
            result.append(product)
    print(result)
