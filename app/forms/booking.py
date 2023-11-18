from django.forms import ModelForm, TextInput, CheckboxInput, Select, DateInput, DateTimeInput, TimeInput, Textarea, SelectMultiple, CharField, PasswordInput, HiddenInput
from django.forms import CharField, ModelMultipleChoiceField, ModelChoiceField
from app.models import Booking, Service, Employee, Client
from config.models import Type


class CreateBookingForm(ModelForm):
    service = ModelMultipleChoiceField(queryset=Service.objects.all(), widget=SelectMultiple(), required=True)

    class Meta:
        model = Booking
        fields = ['client_name', 'client', 'schedule_date', 'schedule_time', 'phone_no', 'client_remark', 'prefered_employee']
        widgets = {
            'client_name': TextInput(attrs={'class': 'form-control'}),
            'client': Select(),
            'schedule_date': DateInput(attrs={'class': 'form-control date-picker'}),
            'schedule_time': TimeInput(attrs={'class': 'form-control time-picker'}),
            'phone_no': TextInput(attrs={'class': 'form-control'}),
            'client_remark': Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'prefered_employee': Select(),
        }


class UpdateBookingForm(ModelForm):
    service = ModelMultipleChoiceField(queryset=Service.objects.all(), widget=SelectMultiple(), required=True)

    class Meta:
        model = Booking
        fields = ['client_name', 'client', 'schedule_date', 'schedule_time', 'phone_no', 'client_remark', 'prefered_employee', 'status',
                  'schedule_remark', 'schedule_employee', 'schedule_start_datetime', 'schedule_end_datetime', 'is_active']
        widgets = {
            'client_name': TextInput(attrs={'class': 'form-control'}),
            'client': Select(),
            'schedule_date': DateInput(attrs={'class': 'form-control date-picker'}),
            'schedule_time': TimeInput(attrs={'class': 'form-control time-picker'}),
            'phone_no': TextInput(attrs={'class': 'form-control'}),
            'client_remark': TextInput(attrs={'class': 'form-control'}),
            'prefered_employee': Select(),
            'status': Select(),
            'schedule_remark': TextInput(attrs={'class': 'form-control'}),
            'schedule_employee': Select(),
            'schedule_start_datetime': DateTimeInput(attrs={'class': 'form-control'}),
            'schedule_end_datetime': DateTimeInput(attrs={'class': 'form-control'}),
            'location': Select(),
            'is_active': CheckboxInput(attrs={'class': 'custom-control-input'}),
            'create_date': TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }


class ClientSelectWidget(Select):

    def create_option(self, name, value, *args, **kwargs):
        option = super().create_option(name, value, *args, **kwargs)
        if value:
            # get instance
            instance = self.choices.queryset.get(client_id=value)
            # set option attributes
            option['attrs']['phone_no'] = instance.phone_no
            option['attrs']['name'] = '{} {}'.format(instance.first_name, instance.last_name)
        return option



class CreateClientBookingForm(ModelForm):
    service = ModelMultipleChoiceField(queryset=Service.objects.all(), widget=SelectMultiple(), required=True)

    class Meta:
        model = Booking
        fields = ['client_name', 'client', 'phone_no', 'client_remark', 'prefered_employee']
        widgets = {
            'client_name': TextInput(attrs={'class': 'form-control'}),
            'client': ClientSelectWidget(),
            'phone_no': TextInput(attrs={'class': 'form-control'}),
            'client_remark': Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'prefered_employee': Select()
        }


class ViewClientBookingForm(ModelForm):
    service = ModelMultipleChoiceField(queryset=Service.objects.all(), widget=SelectMultiple(attrs={'class': 'form-control', 'readonly': True}), required=True)

    class Meta:
        model = Booking
        fields = ['client_name', 'client', 'phone_no', 'client_remark', 'prefered_employee']
        widgets = {
            'client_name': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'client': Select(attrs={'class': 'form-control', 'readonly': True}),
            'phone_no': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'client_remark': Textarea(attrs={'class': 'form-control', 'rows': 2, 'readonly': True}),
            'prefered_employee': Select(attrs={'class': 'form-control', 'readonly': True})
        }
