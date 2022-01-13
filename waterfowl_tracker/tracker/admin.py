from django.contrib.gis import admin

from .models import FarmLoc, Notification, Profile

admin.site.register(FarmLoc, admin.GISModelAdmin)
admin.site.register(Notification)
admin.site.register(Profile)