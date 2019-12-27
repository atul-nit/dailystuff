from django.urls import path
from . import views

app_name = 'search_service'

urlpatterns = [
    path('', views.fullPageResult, name='fullPageResult'),
]