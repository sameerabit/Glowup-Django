from app.models import CustomerUser, Customer, CustomerLocation, ServiceCategory, Service
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


def get_customer_of_user(request):
    return Customer.objects.get(customer_id=CustomerUser.objects.get(user=request.user).customer_id)


def bind_customer_user(customer, user):
    dafault_username = customer.customer_name.replace(' ', '_')
    default_password = get_random_string(length=10)
    user = User.objects.create_user(username=dafault_username,  password=default_password,  email=customer.admin_email, extra_fields={'first_name': customer.customer_name, 'last_name': 'Administrator'})
    CustomerUser.objects.create(customer=customer, user=user, is_salon_admin=True)


def get_location_of_user(request):
    return CustomerLocation.objects.get(location_id=CustomerUser.objects.get(user=request.user).location_id)
