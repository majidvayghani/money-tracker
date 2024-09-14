from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.create_user, name='create_user'),
    path('auth/login/', views.login_user, name='login_user'),
]
