from django.contrib import admin
from crm.models import User, Client
from django.contrib.auth.models import Group

# Register your models here.


# Model registered on admin panel
admin.site.register(User)
admin.site.register(Client)

# Model unregistered on admin panel
admin.site.unregister(Group)


# Modify title and header of site
admin.site.site_header = "Epic Events Administration"
admin.site.site_title = "Epic Events"
