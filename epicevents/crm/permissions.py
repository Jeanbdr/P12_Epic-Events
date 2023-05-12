from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


# Here we will set our permissions for the api
class EmployeeListPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        else:
            return False


class SignupPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST" and request.user.role == "MANAGEMENT":
            return True
        else:
            return False


class CustomersAndContractPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST" and request.user.role == "SALES":
            return True
        if request.method == "GET":
            return True
        if request.method == "DELETE":
            return False
        if request.method in ("PATCH", "UPDATE") and request.user.role in (
            "MANAGEMENT",
            "SALES",
        ):
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in ("PATCH", "UPDATE"):
            return (
                request.user.role == "MANAGEMENT" or obj.sales_contact == request.user
            )


class EventPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "PATCH", "UPDATE"):
            return True
        if request.method == "DELETE":
            return False
        if request.method == "POST" and request.user.role == "SALES":
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in ("PATCH", "UPDATE") and obj.event_status == "COMING":
            return (
                request.user.role == "MANAGEMENT"
                or obj.contract.sales_contact == request.user
                or obj.support_contact == request.user
            )
