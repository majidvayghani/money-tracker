from django.urls import path

from .views import TransactionDetail, TransactionCreateView

urlpatterns = [
    path('', TransactionDetail.as_view(), name = 'transaction-list'),
    path('create', TransactionCreateView.as_view(), name = 'transaction-list'),
    path('<uuid:pk>', TransactionDetail.as_view(),name = 'transaction-detail'),
]