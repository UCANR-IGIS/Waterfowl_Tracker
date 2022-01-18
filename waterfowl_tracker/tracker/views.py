from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from .forms import ProfileForm, form_validation_error
from .models import Profile

from .forms import NotificationForm, form_validation_error
from .models import Notification, FarmLoc


# Create your views here.
def index(request):
    return render(request, 'index.html')

def farms(request):  
    farms = FarmLoc.objects.all()  
    return render(request,"farms.html",{'farms':farms})

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

@method_decorator(login_required(login_url='login'), name='dispatch')
class NotificationView(View):
    notification = None

    def dispatch(self, request, *args, **kwargs):
        self.notification, __ = Notification.objects.get_or_create(owner=request.user)
        return super(NotificationView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {'notification': self.notification, 'segment': 'notification'}
        return render(request, 'notifications.html', context)

    def post(self, request):
        #farmloc = FarmLoc.objects.filter(owner_id=1)
        #farmloc.
        '''farms = request.POST.getlist('farm')
        #farms = [int(i) for i in project_users]

        tempdict = self.request.POST.copy()

        if 'owner_id' in tempdict.keys():
            tempdict['owner'] = int(tempdict['owner'])

        if 'alerts' in tempdict.keys():
            tempdict['alerts'] = True
        else:
            tempdict['alerts'] = False

        if 'low_dens' in tempdict.keys():
            tempdict['low_dens'] = True
        else:
            tempdict['low_dens'] = False

        if 'med_dens' in tempdict.keys():
            tempdict['med_dens'] = True
        else:
            tempdict['med_dens'] = False

        if 'high_dens' in tempdict.keys():
            tempdict['high_dens'] = True
        else:
            tempdict['high_dens'] = False

        if 'on_prop' in tempdict.keys():
            tempdict['on_prop'] = True
        else:
            tempdict['on_prop'] = False

        if 'two_km' in tempdict.keys():
            tempdict['two_km'] = True
        else:
            tempdict['two_km'] = False

        if 'five_km' in tempdict.keys():
            tempdict['five_km'] = True
        else:
            tempdict['five_km'] = False

        if 'ten_km' in tempdict.keys():
            tempdict['ten_km'] = True
        else:
            tempdict['ten_km'] = False

        tempdict['farm'] = farms

        self.request.POST = tempdict  # this is the added line'''
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
        return redirect('notifications')