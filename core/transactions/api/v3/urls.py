from django.urls import path

from .views import TransactionDetail

urlpatterns = [
    path('', TransactionDetail.as_view(), name = 'transaction-list'),
    path('<uuid:pk>', TransactionDetail.as_view(),name = 'transaction-detail'),
]