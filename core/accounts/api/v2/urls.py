from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginAuthToken.as_view(), name='token-login'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('logout/', views.LogoutView.as_view(), name='api-logout'),
]
