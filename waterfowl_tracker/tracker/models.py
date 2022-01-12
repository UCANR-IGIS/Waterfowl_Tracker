from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


intType = [
    ('Always', 'Always'),
    ('Detect', 'Only when waterfowl are detected')
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

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

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    pnt = models.PointField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name        

class Notification(models.Model):
    alerts = models.BooleanField('Email Alerts', default=False)
    low_dens = models.BooleanField('Low Density', default=False)
    med_dens = models.BooleanField('Medium Density', default=False)
    high_dens = models.BooleanField('High Density', default=False)
    on_prop = models.BooleanField('On Property', default=False)
    two_km = models.BooleanField('2 km Radius', default=False)
    five_km = models.BooleanField('5 km Radius', default=False)
    ten_km = models.BooleanField('10 km Radius', default=False)
    daily = models.CharField('Daily', max_length=50, choices=intType)
    weekly = models.CharField('Weekly', max_length=50, choices=intType)
    emails = models.CharField('Alert Emails (separate with comma)', max_length=250, default='')
    farm = models.ManyToManyField(FarmLoc)
