from django.contrib import admin
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


# Register other elements
admin.site.register(Client)
admin.site.register(Event)
admin.site.register(Contract)

# Model unregistered on admin panel
admin.site.unregister(Group)


# Modify title and header of site
admin.site.site_header = "Epic Events Administration"
admin.site.site_title = "Epic Events"
