from django.urls import path

from .views import *


urlpatterns = [
    path('signin', SigninAuthToken.as_view(), name='signin'),
    path('signup', SignupAPIview.as_view(), name='signup'),
    path('user', UserGetOrUpdateOrDeleteAPIView.as_view(), name='user'),
    path('signout', SignoutAPIView.as_view(), name='signout'),
    path('profile', ProfileGetOrUpdateOrDeleteAPIView.as_view(), name='profile'),
]