from django.shortcuts import render, get_object_or_404
from .models import Order

def thanksPage(request, orderId):
    customerOrder = None
    if orderId:
        customerOrder = get_object_or_404(Order, id=orderId)
    return render(request, 'thankspage.html', {'customer_order': customerOrder})
