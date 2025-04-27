from django.urls import path

from .views import *

urlpatterns = [
    path('', TransactionDetail.as_view(), name = 'transaction-list'),
    path('create', TransactionCreateView.as_view(), name = 'transaction-list'),
    path('<uuid:pk>', TransactionDetail.as_view(),name = 'transaction-detail'),
    path('categories', Category.as_view(), name='category-list'),
    path('categories/<uuid:pk>/', CategoryDetail.as_view(), name='category-detail'),
]