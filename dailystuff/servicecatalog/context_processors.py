from .models import ServiceCategory

def servicecategory_links(request):
    menulinks = ServiceCategory.objects.all()
    return dict(menulinks=menulinks)


