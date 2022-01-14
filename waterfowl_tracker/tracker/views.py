from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from .forms import ProfileForm, form_validation_error
from .models import Profile

from .forms import NotificationForm, form_validation_error
from .models import Notification


# Create your views here.
def index(request):
    return render(request, 'index.html')

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
        form = NotificationForm(request.POST, request.FILES, instance=self.notification)

        if form.is_valid():
            notification = form.save()
            notification.save()

            messages.success(request, 'Notification saved successfully')
        else:
            messages.error(request, form_validation_error(form))
        return redirect('notification')