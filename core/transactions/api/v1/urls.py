from django.contrib import admin
from django.urls import path

from .views import transaction_list, transaction_detail

urlpatterns = [
    path('', transaction_list, name = 'transaction-list'),
    path('<uuid:pk>', transaction_detail, name = 'transaction-detail'),
]