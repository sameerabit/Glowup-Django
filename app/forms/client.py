from django.forms import ModelForm, TextInput, NumberInput, EmailInput, Select, CheckboxInput, HiddenInput, Textarea, CharField, PasswordInput, ModelChoiceField, DateInput, ModelMultipleChoiceField, SelectMultiple, FileField, ClearableFileInput, BooleanField
from app.models import Client, ClientSession, Employee, Booking, Service


class CreateClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['registration_no', 'first_name', 'last_name', 'postal_code', 'email', 'phone_no', 'introduced_by']
        widgets = {
            'registration_no': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'postal_code': NumberInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'phone_no': TextInput(attrs={'class': 'form-control'}),
            'introduced_by': Select()
        }


class UpdateClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['registration_no', 'first_name', 'last_name', 'postal_code', 'email', 'phone_no', 'introduced_by', 'is_active']
        widgets = {
            'registration_no': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'postal_code': NumberInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'phone_no': TextInput(attrs={'class': 'form-control'}),
            'is_active': CheckboxInput(attrs={'class': 'custom-control-input'}),
            'introduced_by': TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
        }


class ClientSessionStartForm(ModelForm):
    schedule_remark = CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), label="Remarks")
    employee_id = ModelChoiceField(widget=Select(), label="Employee", queryset=Employee.objects.all())
    passcode = CharField(widget=PasswordInput(attrs={'class': 'form-control'}), label="Employee Passcode")

    class Meta:
        model = ClientSession
        fields = ['personal_style', 'professional_style', 'personal_interests', 'hair_goals', 'commitment', 'time_spending', 'versality', 'styling_preferences',
                  'comfort_level', 'preferences', 'products', 'abudance', 'diameter', 'hair_formation', 'condition', 'face_type', 'distress', 'skin_tone', 'chemical_service']
        widgets = {
            'personal_style': Select(),
            'professional_style': Select(),
            'personal_interests': Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'hair_goals': Select(),
            'commitment': Select(),
            'time_spending': Select(),
            'versality': Select(),
            'styling_preferences': Select(),
            'comfort_level': Select(),
            'preferences': Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'products': Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'abudance': Select(),
            'diameter': Select(),
            'hair_formation': Select(),
            'condition': Select(),
            'face_type': Select(),
            'distress': Select(),
            'skin_tone': Select(),
            'chemical_service': Select()
        }


class ClientSessionEndForm(ModelForm):
    services = ModelMultipleChoiceField(queryset=Service.objects.all(), widget=SelectMultiple())
    passcode = CharField(widget=PasswordInput(attrs={'class': 'form-control', 'autocomplete':'off'}), label="Employee Passcode")
    attachments = FileField(widget=ClearableFileInput(attrs={'class': 'form-control', 'multiple': True}), required=False)
    todo_type = CharField(required=True, widget=HiddenInput())
    register_as_new = BooleanField(required=False, widget=CheckboxInput(), label="Register as a New Client")

    class Meta:
        model = Booking
        fields = ['client_name', 'schedule_date', 'phone_no', 'client_remark', 'schedule_remark']
        widgets = {
            'client_name': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'schedule_date': DateInput(attrs={'class': 'form-control', 'readonly': True}),
            'phone_no': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'client_remark': Textarea(attrs={'class': 'form-control', 'rows': 2, 'readonly': True}),
            'schedule_remark': Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
