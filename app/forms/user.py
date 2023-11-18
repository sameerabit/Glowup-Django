from django.forms import ModelForm, TextInput, CheckboxInput, EmailInput, DateInput, PasswordInput, ModelChoiceField, Select, ChoiceField
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User, Group
from config.models import CustomerLocation
import pytz

def timezones():
    timezones = []
    for _tz in pytz.common_timezones:
        timezones.append((_tz,_tz))
    return timezones
time_zones = timezones()

class CreateUserForm(UserCreationForm):
    location = ModelChoiceField(queryset=CustomerLocation.objects.all(), widget=Select())
    user_type = ModelChoiceField(queryset=Group.objects.all(), widget=Select())
    time_zone = ChoiceField(choices=time_zones, widget=Select())

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class UpdateUserForm(UserChangeForm):
    location = ModelChoiceField(queryset=CustomerLocation.objects.all(), widget=Select())
    user_type = ModelChoiceField(queryset=Group.objects.all(), widget=Select())
    time_zone = ChoiceField(choices=time_zones, widget=Select())

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'date_joined', 'last_login', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_joined'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_login'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_active'].widget.attrs.update({'class': 'custom-control-input'})
        self.fields['password'].help_text = ("Raw passwords are not stored, so there is no way to see this "
                                             "user's password, but you can change the password using "
                                             "<a href='password'>this form</a>.")


class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})
