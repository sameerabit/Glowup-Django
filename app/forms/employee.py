from django.forms import ModelForm, TextInput, CheckboxInput, Select, ModelChoiceField, PasswordInput, ModelMultipleChoiceField, SelectMultiple
from app.models import Employee, Service
from config.models import CustomerLocation


class CreateEmployeeForm(ModelForm):
    location = ModelChoiceField(queryset=CustomerLocation.objects.all(), widget=Select())
    services = ModelMultipleChoiceField(queryset=Service.objects.all(), widget=SelectMultiple())

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'passcode']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'passcode': PasswordInput(attrs={'class': 'form-control'})
        }


class UpdateEmployeeForm(ModelForm):
    location = ModelChoiceField(queryset=CustomerLocation.objects.all(), widget=Select())
    services = ModelMultipleChoiceField(queryset=Service.objects.all(), widget=SelectMultiple())

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'is_active']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'is_active': CheckboxInput(attrs={'class': 'custom-control-input'}),
        }