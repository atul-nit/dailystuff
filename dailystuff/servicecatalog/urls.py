from django.urls import path
from . import views

app_name = 'servicecatalog'

urlpatterns = [
    path('home/', views.allServiceProducts, name='allServices'),
    path('services/<slug:s_url_key>/', views.serviceByCategory, name='serviceByCategory'),
    path('service/<slug:service_cat_url_key>/<slug:service_prod_url_key>/',
         views.serviceDetail, name="serviceDetail"),
    path('accounts/create/', views.loginView, name='loginview'),
]