from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.models import Group, User
from .models import ServiceCategory, ServiceProduct
from .forms import RegisterForm


def allServiceProducts(request):
    " Get All Service Products "
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

def serviceByCategory(request, s_url_key):
    " Get Service Products by Service Category"
    s_page = get_object_or_404(ServiceCategory, url_key=s_url_key)
    service_list = ServiceProduct.objects.raw(
        'SELECT * FROM servicecatalog_serviceproduct where is_available=1 '
        'and servicecategory_id={}'.format(s_page.id)
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
    return render(request, 'servicecatalog/services.html', {'category': s_page, 'services': services})

def registerView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            register_user = User.objects.get(username=username)
            user_group = Group.objects.get(name='Customer')
            user_group.user_set.add(register_user)
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

