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
    EmployeeViewSet,
)


def trigger_error(request):
    # Function used to ensure the proper functioning of Sentry
    division_by_zero = 1 / 0


router = routers.SimpleRouter()
router.register("clients", ClientViewSet, basename="clients")

contract_router = routers.SimpleRouter()
contract_router.register("contract", ContractViewSet, basename="contract")

contract_nested_router = routers.NestedSimpleRouter(router, "clients", lookup="clients")
contract_nested_router.register(r"contract", ContractViewSet, basename="contract")

event_router = routers.SimpleRouter()
event_router.register("event", EventViewSet, basename="event")

event_nested_router = routers.NestedSimpleRouter(
    contract_nested_router, "contract", lookup="contract"
)
event_nested_router.register(r"event", EventViewSet, basename="event")

employee_router = routers.SimpleRouter()
employee_router.register("employees", EmployeeViewSet, basename="employees")

signup_router = routers.SimpleRouter()
signup_router.register("create_user", SignupViewSet, basename="create_user")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("", include(contract_router.urls)),
    path("", include(event_router.urls)),
    path("", include(signup_router.urls)),
    path("login", ObtainTokainPairView.as_view(), name="obtain_token"),
    path("login/refresh", TokenRefreshView.as_view(), name="refresh_token"),
    path("", include(contract_nested_router.urls)),
    path("", include(event_nested_router.urls)),
    path("sentry-debug/", trigger_error),
    path("", include(employee_router.urls)),
]
