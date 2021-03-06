from django.contrib.gis.db import models
from django.contrib.auth.models import User

intType = [
    ('Always', 'Always'),
    ('Detect', 'Only when waterfowl are detected')
]
freqType = [
    ('daily', 'Daily'),
    ('weekly', 'Weekly')
]

class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="profiles/avatars/", null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else 'https://github.com/mdo.png'

class FarmLoc(models.Model):
    name = models.CharField('Farm Name', max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    prod_type = models.CharField('Production Type', max_length=100)
    farm_type = models.CharField('Farm Type', max_length=100)
    lon = models.FloatField()
    lat = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # GeoDjango-specific: a geometry field
    pnt = models.PointField()

    class Meta:
        verbose_name = 'Farm'
        verbose_name_plural = 'Farms'

    # Returns the string representation of the model.
    def __str__(self):
        return self.name        

class Notification(models.Model):
    name = models.CharField('Notification Name', max_length=100, default='')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    alerts = models.BooleanField('Email Alerts', default=False)
    low_dens = models.BooleanField('Low Density', default=False)
    med_dens = models.BooleanField('Medium Density', default=False)
    high_dens = models.BooleanField('High Density', default=False)
    on_prop = models.BooleanField('On Property', default=False)
    two_km = models.BooleanField('2 km Radius', default=False)
    five_km = models.BooleanField('5 km Radius', default=False)
    ten_km = models.BooleanField('10 km Radius', default=False)
    interval = models.CharField('Waterfowl Presence', max_length=50, choices=intType)
    reportfreq = models.CharField('Report Frequency', max_length=50, choices=freqType)
    emails = models.CharField('Alert Emails (separate with comma)', max_length=250, default='')
    farm = models.ManyToManyField(FarmLoc)

class FarmWaterfowlDensities(models.Model):
    date1   = models.DateField()
    farm_id = models.BigIntegerField(primary_key=True,)
    owner_id = models.BigIntegerField()
    name = models.CharField('Farm Name', max_length=100)
    lon = models.FloatField()
    lat = models.FloatField()
    density_onfarm = models.CharField('Waterfowl density on farm', max_length=10)
    density_2km = models.CharField('Waterfowl density within 2km of farm', max_length=10)
    density_5km = models.CharField('Waterfowl density within 5km of farm', max_length=10)
    density_10km = models.CharField('Waterfowl density within 10km of farm', max_length=10)

    class Meta:
        managed = False
        db_table='farmsmodel'

class FarmBuffer(models.Model):
    id = models.BigIntegerField(primary_key=True,)
    parent_id = models.BigIntegerField()
    owner_id = models.BigIntegerField()
    dist1 = models.CharField('Distance', max_length=100)
    geometry = models.PolygonField()

    class Meta:
        managed = False
        db_table='farmsbuffer'

class RasterLinks(models.Model):
    id = models.BigIntegerField(primary_key=True, )
    filedate = models.CharField('Date', max_length=100)
    linkname = models.CharField('Link', max_length=100)


    class Meta:
        managed = False
        db_table='raster_links'