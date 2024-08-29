from django.contrib import admin
from django.urls import path

from .views import transaction_list, transaction_detail

urlpatterns = [
    path('transactions/', transaction_list, name = 'transaction-list'),
    path('transactions/<uuid:pk>/', transaction_detail, name = 'transaction-detail'),
]