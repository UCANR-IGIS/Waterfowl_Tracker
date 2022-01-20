from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from .models import FarmLoc, Notification, Profile

admin.site.register(FarmLoc, LeafletGeoAdmin)
admin.site.register(Notification)
admin.site.register(Profile)