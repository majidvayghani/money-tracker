from django.urls import path


from . import views

urlpatterns = [
    path('login/', views.LoginAuthToken.as_view(), name='token-login')
]
