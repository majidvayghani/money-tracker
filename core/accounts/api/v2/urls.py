from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token


from . import views

urlpatterns = [
    path('auth/register/', views.create_user, name='create-user'),
    # path('auth/login/', views.login_user_v1, name='login-user'),
    path('auth/login/', views.CustomAuthToken.as_view(), name='token-login')
]
