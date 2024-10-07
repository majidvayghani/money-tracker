"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django routes
    path('ping', include('health.urls'), name = 'health_ping'),
    path('admin/', admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),

    # API routes
    path('api/v1/users/', include('accounts.api.v1.urls'), name = 'account_api_v1'),
    path('api/v1/transactions/', include('transactions.api.v1.urls'), name = 'transaction_api_v1'),

    path('api/v2/users/', include('accounts.api.v2.urls'), name = 'account_api_v2'),
    path('api/v2/transactions/', include('transactions.api.v2.urls'), name = 'transaction_api_v2'),

    # path('api/v3/users/', include('accounts.api.v3.urls'), name = 'account_api_v3'),
    path('api/v3/transactions/', include('transactions.api.v3.urls'), name = 'transaction_api_v3'),

]