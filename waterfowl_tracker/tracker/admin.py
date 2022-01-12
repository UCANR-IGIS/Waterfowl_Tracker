from django.contrib.gis import admin

from .models import FarmLoc, Notification

admin.site.register(FarmLoc, admin.GISModelAdmin)
admin.site.register(Notification)
