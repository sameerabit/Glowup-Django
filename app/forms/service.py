from django.forms import ModelForm, TextInput, NumberInput, EmailInput, Select, CheckboxInput, DateTimeField, SelectMultiple
from app.models import Service, EmployeeService


class ServiceCreateForm(ModelForm):
    class Meta:
        model = Service
        fields = ['service_name', 'price', 'service_category']
        widgets = {
            'service_name': TextInput(attrs={'class': 'form-control'}),
            'price': NumberInput(attrs={'class': 'form-control'}),
            'service_category': Select(),
        }


class ServiceUpdateForm(ModelForm):
    class Meta:
        model = Service
        fields = ['service_name', 'price', 'service_category']
        widgets = {
            'service_name': TextInput(attrs={'class': 'form-control'}),
            'price': NumberInput(attrs={'class': 'form-control'}),
            'service_category': Select(),
            'is_active': CheckboxInput(attrs={'class': 'custom-control-input'}),
            'create': TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }


class ServiceAssignForm(ModelForm):
    class Meta:
        model = EmployeeService
        fields = ['employee', 'service']
        widgets = {
            'service': SelectMultiple(),
            'employee': Select()
        }


class ServiceDeAllocateForm(ModelForm):
    class Meta:
        model = EmployeeService
        fields = ['employee', 'service', 'is_active', 'create']
        widgets = {
            'service': SelectMultiple(),
            'employee': Select(),
            'is_active': CheckboxInput(attrs={'class': 'custom-control-input'}),
            'create': TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }
