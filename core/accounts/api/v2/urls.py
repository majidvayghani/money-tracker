from django.urls import path

from .views import SigninAuthToken, SignupAPIview, UserGetOrUpdateOrDeleteAPIView, SignoutAPIView

urlpatterns = [
    path('signin', SigninAuthToken.as_view(), name='signin'),
    path('signup', SignupAPIview.as_view(), name='signup'),
    path('signout', SignoutAPIView.as_view(), name='signout'),
    path('profile', UserGetOrUpdateOrDeleteAPIView.as_view(), name='profile'),
]
