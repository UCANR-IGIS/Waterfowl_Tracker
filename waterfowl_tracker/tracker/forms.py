from django.contrib.gis import forms
from .models import FarmLoc, Profile
from .models import Notification
from .models import FarmLoc


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']

class NotificationForm(forms.ModelForm):
    #farmsall = forms.ModelMultipleChoiceField(queryset=FarmLoc.objects.all())
    #farmsall = forms.ModelMultipleChoiceField(None)
    class Meta:
        model = Notification
        fields = '__all__'
        exclude = ['user']#,'farm']

    #farmsall = forms.ModelMultipleChoiceField(queryset=None)

    #def __init__(self, *args, **kwargs):
    #    super(NotificationForm, self).__init__(*args, **kwargs)
    #    self.fields['farmsall'].queryset = farmsall.objects.filter(queryset=None)

class FarmForm(forms.ModelForm):  
    name = forms.CharField()
    address = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    prod_type = forms.CharField()
    farm_type = forms.CharField()
    lon = forms.FloatField()
    lat = forms.FloatField()
    #owner = forms.ForeignKey()

    # GeoDjango-specific: a geometry field
    pnt = forms.PointField(widget=
        forms.OSMWidget(attrs={'map_width': 800,
            'map_height': 500,
            "default_lat": 37.158517,
            "default_lon":  -119.938244,
            "default_zoom": 6}))
        
    class Meta:
        model = FarmLoc
        fields = '__all__'
        exclude = ['user']

def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg