from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from .models import ServiceCategory, ServiceProduct


def allServiceProducts(request):
    service_list = ServiceProduct.objects.raw(
        'SELECT * FROM servicecatalog_serviceproduct where is_available=1'
    )
    paginator = Paginator(service_list, 6)
    try:
        page_num = int(request.GET.get('page', 1))
    except:
        page_num = 1
    try:
        services = paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        services = paginator.page(paginator.num_pages)
    return render(request, 'servicecatalog/services.html', {'category': None, 'services': services})