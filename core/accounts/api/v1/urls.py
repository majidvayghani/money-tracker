from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.create_user, name='create_user'),
    #path('user/<int:pk>/', views.get_user, name='get_user'),
]
