from django import forms
from .models import Profile
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


def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg