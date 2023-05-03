from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


# Here we will set our permissions for the api
class CustomersAndContractPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST" and request.user.role == "SALES":
            return True

        if request.method == "GET" and request.user.role in (
            "SALES",
            "MANAGEMENT",
            "SUPPORT",
        ):
            return True

        if request.method == "DELETE" and request.user.role in (
            "SALES",
            "MANAGEMENT",
            "SUPPORT",
        ):
            return False

        if request.method in ("PATCH", "UPDATE") and request.user.role == "MANAGEMENT":
            return True

    def has_object_permission(self, request, view, obj):
        if (
            request.method in ("PATCH", "UPDATE")
            and obj.sales_contact == self.request.user
        ):
            return True


class EventPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET" and request.user.role in (
            "SALES",
            "MANAGEMENT",
            "SUPPORT",
        ):
            return True
        if request.method == "DELETE" and request.user.role in (
            "SALES",
            "MANAGEMENT",
            "SUPPORT",
        ):
            return False
        if request.method == "POST" and request.user.role == "SALES":
            return True

        if request.method in ("PATCH", "UPDATE") and request.user.role == "MANAGEMENT":
            return True

    def has_object_permission(self, request, view, obj):
        if (
            request.method in ("PATCH", "UPDATE")
            and obj.sales_contact
            or obj.support_contact == self.request.user
        ):
            return True
