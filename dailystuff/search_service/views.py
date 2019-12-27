from django.shortcuts import render
from servicecatalog.models import ServiceProduct
from django.db.models import Q

def fullPageResult(request):
    services = None
    search_query = None
    if 'q' in request.GET:
        search_query = request.GET['q']
        services = ServiceProduct.objects.all().filter(
            Q(product_name__contains = search_query) | Q(description__contains = search_query))
        print(services)
    return render(request, 'searchresults.html', {'query': search_query, 'services': services})
