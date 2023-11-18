from django.forms import ModelForm, TextInput, CheckboxInput, Select
from app.models import ServiceCategory


class CreateServiceCategoryForm(ModelForm):
    class Meta:
        model = ServiceCategory
        fields = ['service_category_name']
        widgets = {
            'service_category_name': TextInput(attrs={'class': 'form-control'}),
        }


class UpdateServiceCategoryForm(ModelForm):
    class Meta:
        model = ServiceCategory
        fields = ['service_category_name', 'is_active', 'create']
        widgets = {
            'service_category_name': TextInput(attrs={'class': 'form-control'}),
            'is_active': CheckboxInput(attrs={'class': 'custom-control-input'}),
            'create': TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }
