"""
URL configuration for epicevents project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from rest_framework import routers
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenRefreshView

from crm.views import (
    SignupViewSet,
    ClientViewSet,
    ObtainTokainPairView,
    ContractViewSet,
    EventViewSet,
)

router = routers.SimpleRouter()
router.register("clients", ClientViewSet, basename="clients")

contract_router = routers.NestedSimpleRouter(router, "clients", lookup="clients")
contract_router.register(r"contract", ContractViewSet, basename="contract")

event_router = routers.NestedSimpleRouter(router, "clients", lookup="clients")
event_router.register(r"event", EventViewSet, basename="event")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("registration", SignupViewSet.as_view(), name="registration"),
    path("login", ObtainTokainPairView.as_view(), name="obtain_token"),
    path("login/refresh", TokenRefreshView.as_view(), name="refresh_token"),
    path("", include(contract_router.urls)),
]
