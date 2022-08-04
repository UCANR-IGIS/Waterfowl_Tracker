from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from .forms import ProfileForm, form_validation_error
from .models import Profile

from .forms import NotificationForm, FarmForm, form_validation_error
from .models import Notification, FarmLoc, FarmWaterfowlDensities, FarmBuffer, RasterLinks

from django.db import transaction, connection
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

#@receiver(post_save, sender=FarmLoc)
#def refresh_view(sender, **kwargs):
#    with connection.cursor() as cursor:
#        cursor.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY farmsmodel")

#@receiver(post_delete, sender=FarmLoc)
#def refresh_view(sender, **kwargs):
#    with connection.cursor() as cursor:
#        cursor.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY farmsmodel")

# Create your views here.
def index(request):
    min_date = FarmWaterfowlDensities.objects.earliest('date1').date1.strftime('%B %d, %Y')
    max_date = FarmWaterfowlDensities.objects.latest('date1').date1.strftime('%B %d, %Y')
    rasters = serializers.serialize("json", RasterLinks.objects.all())
    return render(request, 'index.html', {'rasters': rasters, 'max_date': max_date, 'min_date': min_date})

def app(request):
    min_date = FarmWaterfowlDensities.objects.earliest('date1').date1.strftime('%B %d, %Y')
    max_date = FarmWaterfowlDensities.objects.latest('date1').date1.strftime('%B %d, %Y')
    farms = serializers.serialize("json", FarmWaterfowlDensities.objects.filter(owner_id=request.user.id))
    rasters = serializers.serialize("json", RasterLinks.objects.all())
    return render(request, 'app.html', {'farms': farms, 'rasters': rasters, 'max_date': max_date, 'min_date': min_date})

def appAdmin(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('app'))
    min_date = FarmWaterfowlDensities.objects.earliest('date1').date1.strftime('%B %d, %Y')
    max_date = FarmWaterfowlDensities.objects.latest('date1').date1.strftime('%B %d, %Y')
    farms = serializers.serialize("json", FarmWaterfowlDensities.objects.all())
    rasters = serializers.serialize("json", RasterLinks.objects.all())
    return render(request, 'appAdmin.html', {'farms': farms, 'rasters': rasters, 'max_date': max_date, 'min_date': min_date})

def farm_json(request):
    farms_pnts = serializers.serialize('geojson', FarmLoc.objects.filter(owner=request.user.id),
                                       geometry_field='pnt',
                                       fields=('name',))
    return HttpResponse(farms_pnts, content_type='application/json')

def buffer_json(request):
    farms_buffers = serializers.serialize('geojson', FarmBuffer.objects.filter(owner_id=request.user.id),
                                       geometry_field='geometry',
                                       fields=('parent_id', 'dist1',))
    return HttpResponse(farms_buffers, content_type='application/json')

def farm_json_admin(request):
    farms_pnts = serializers.serialize('geojson', FarmLoc.objects.all(),
                                       geometry_field='pnt',
                                       fields=('name',))
    return HttpResponse(farms_pnts, content_type='application/json')

def buffer_json_admin(request):
    farms_buffers = serializers.serialize('geojson', FarmBuffer.objects.all(),
                                       geometry_field='geometry',
                                       fields=('parent_id', 'dist1',))
    return HttpResponse(farms_buffers, content_type='application/json')


def farms(request):  
    farms = FarmLoc.objects.filter(owner=request.user)  
    return render(request, "farms.html", {'farms': farms})

def notifications(request):
    notifications = Notification.objects.filter(owner=request.user)
    return render(request, "notification.html", {'notifications': notifications})

@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfileView(View):
    profile = None

    def dispatch(self, request, *args, **kwargs):
        self.profile, __ = Profile.objects.get_or_create(user=request.user)
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {'profile': self.profile, 'segment': 'profile'}
        return render(request, 'profile.html', context)

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=self.profile)

        if form.is_valid():
            profile = form.save()
            profile.user.first_name = form.cleaned_data.get('first_name')
            profile.user.last_name = form.cleaned_data.get('last_name')
            profile.user.email = form.cleaned_data.get('email')
            profile.user.save()

            messages.success(request, 'Profile saved successfully')
        else:
            messages.error(request, form_validation_error(form))
        return redirect('profile')

'''@method_decorator(login_required(login_url='login'), name='dispatch')
class NotificationView(View):
    notification = None

    def dispatch(self, request, *args, **kwargs):
        self.notification, __ = Notification.objects.get_or_create(owner=request.user)
        return super(NotificationView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {'notification': self.notification, 'segment': 'notification'}
        return render(request, 'notifications.html', context)

    def post(self, request):
        farms = request.POST.getlist('farm')
        farms = tuple([int(i) for i in farms])

        form = NotificationForm(request.POST, instance=self.notification)
        if not form.is_valid():
            messages.error(request, form_validation_error(form))       
        else:
            notification = form.save(commit=False)

            farmsall = FarmLoc.objects.filter(notification=notification)
            farmsall = farmsall.values_list('pk', flat=True)
            farmsall = tuple([int(i) for i in farmsall])

            if farmsall:
                for i in farmsall:
                    notification.farm.remove(i)
            if farms:
                for i in farms:
                    notification.farm.add(i)

            notification.save()

            messages.success(request, 'Notification saved successfully')
        return redirect('notifications')'''

def NotificationView(request):
    if request.method == "POST":
        form = NotificationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('notification')
            except:
                pass
    else:
        form = NotificationForm()
    return render(request, 'notifications.html', {'form': form})

def addnew(request):  
    if request.method == "POST":  
        form = FarmForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()
                return redirect('farms')
            except:
                pass 
    else:  
        form = FarmForm()  
    return render(request,'addnew.html',{'form':form})  
def edit(request, id):  
    farm = FarmLoc.objects.get(id=id)
    form = FarmForm(instance=farm)
    return render(request,'edit.html', {'form':form,'farm':farm})
def update(request, id):  
    farm = FarmLoc.objects.get(id=id)  
    form = FarmForm(request.POST, instance=farm)
    if form.is_valid():  
        form.save()
        return redirect("farms")
    return render(request, 'edit.html', {'farm': farm})
def destroy(request, id):  
    farm = FarmLoc.objects.get(id=id)  
    farm.delete()  
    return redirect("farms")
def editNotification(request, id):
    notification = Notification.objects.get(id=id)
    form = NotificationForm(instance=notification)
    return render(request, 'editnotification.html', {'form':form, 'notification':notification})
def updateNotification(request, id):
    notification = Notification.objects.get(id=id)
    form = NotificationForm(request.POST, instance=notification)
    if form.is_valid():
        form.save()
        return redirect("notification")
    return render(request, 'editnotification.html', {'notification': notification})
def destroyNotification(request, id):
    notification = Notification.objects.get(id=id)
    notification.delete()
    return redirect("notification")
 
