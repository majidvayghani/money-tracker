from django.urls import path
from .views import PingView

urlpatterns = [
    path('', PingView.as_view(), name='ping'),
    ]