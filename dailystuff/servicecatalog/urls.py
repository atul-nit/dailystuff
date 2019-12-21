from django.urls import path
from . import views

app_name = 'servicecatalog'

urlpatterns = [
    path('home/', views.allServiceProducts, name='allServices'),
]