from typing import Optional
from django.contrib import admin
from django.contrib.admin import site
from django.http.request import HttpRequest
from crm.models import User, Client, Event, Contract
from crm.serializers import SignUpSerializer
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.


# Define a new User Admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    serilizers = SignUpSerializer
    list_display = ("id", "first_name", "last_name", "username", "email", "role")
    fieldsets = BaseUserAdmin.fieldsets
    fieldsets[0][1]["fields"] = fieldsets[0][1]["fields"] + ("role",)
    search_fields = ("username", "email")
    actions = ["delete_selected"]


class EventAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False


class ClientAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False


class ContractAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False


# Register other elements
admin.site.register(Client, ClientAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Contract, ContractAdmin)

# Model unregistered on admin panel
admin.site.unregister(Group)


# Modify title and header of site
admin.site.site_header = "Epic Events Administration"
admin.site.site_title = "Epic Events"

site.disable_action("delete_selected")
