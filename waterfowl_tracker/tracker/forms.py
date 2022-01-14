from django import forms
from .models import Profile
from .models import Notification


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']

class NotificationForm(forms.ModelForm):
    '''alerts = forms.BooleanField()
    low_dens = forms.BooleanField()
    med_dens = forms.BooleanField()
    high_dens = forms.BooleanField()
    on_prop = forms.BooleanField()
    two_km = forms.BooleanField()
    five_km = forms.BooleanField()
    ten_km = forms.BooleanField()
    daily = forms.CharField( max_length=50)
    weekly = forms.CharField(max_length=50)
    emails = forms.CharField(max_length=250)
    farm = forms.MultipleChoiceField()'''

    class Meta:
        model = Notification
        fields = '__all__'
        exclude = ['user']


def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg