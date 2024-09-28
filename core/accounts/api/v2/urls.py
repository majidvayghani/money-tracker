from django.urls import path

from .views import SigninAuthToken, UserProfileAPIView, SignoutAPIView

urlpatterns = [
    path('signin/', SigninAuthToken.as_view(), name='signin'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('signout/', SignoutAPIView.as_view(), name='signout'),
]
