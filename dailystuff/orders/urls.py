from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('thankspage/<int:orderId>/', views.thanksPage, name="thankspage"),
]