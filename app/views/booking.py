from django.shortcuts import render, redirect, get_object_or_404
from django.core.serializers import serialize
from django.http import JsonResponse
from django.contrib import messages
from django.utils.timezone import now
from app.forms.booking import CreateBookingForm, UpdateBookingForm, CreateClientBookingForm
from app.models import Booking, ServiceCategory, Service, Client, ServiceBooking
from app.utils import get_customer_of_user, get_location_of_user
from app.check_auth import permission_required


@permission_required('app.add_future_booking')
def create_booking(request):
    customer = get_customer_of_user(request)
    location = get_location_of_user(request)
    form = CreateBookingForm(request.POST or None, instance=Booking(create=request.user, customer=customer, location=location, token=_get_token_no(customer, location)))

    form.fields['service'].choices = _get_service_of_customer(customer)
    form.fields['client'].queryset = Client.objects.filter(customer=customer)

    if form.is_valid():
        booking = form.save()
        requested_services = request.POST.getlist('service')
        for service in Service.objects.filter(service_id__in=requested_services):
            ServiceBooking.objects.create(booking=booking, service=service)
        messages.success(request, "Your Booking {} has been made for {} service(s)".format(booking.token, len(requested_services)))
        return redirect('view_bookings')
    return render(request, 'booking/create.html', {
        'form': form, 'title': 'Bookings', 'subTitle': 'Create New Booking', 'iconClass': 'fa-clipboard-list'
    })


@permission_required('app.view_future_bookings')
def view_bookings(request):
    return render(request, 'booking/list.html', {
        'bookings': Booking.objects.filter(customer=get_customer_of_user(request), schedule_date__gte=now(), schedule_start_datetime__isnull=True).order_by('schedule_date', 'schedule_start_datetime'), 'title': 'Bookings', 'subTitle': 'List of Bookings', 'iconClass': 'fa-clipboard-list'
    })


@permission_required('app.change_future_booking')
def update_booking(request, booking_id):
    customer = get_customer_of_user(request)
    booking = get_object_or_404(Booking.objects.filter(customer=customer, booking_id=booking_id))
    form = UpdateBookingForm(request.POST or None, instance=booking, initial={
        'service': ServiceBooking.objects.filter(booking=booking).values_list('service_id', flat=True)
    })
    form.fields['service'].choices = _get_service_of_customer(customer)
    form.fields['client'].queryset = Client.objects.filter(customer=customer)
    if form.is_valid():
        ServiceBooking.objects.filter(booking=booking).delete()
        for service in Service.objects.filter(service_id__in=request.POST.getlist('service')):
            ServiceBooking.objects.create(booking=booking, service=service)
        form.save()
        return redirect('view_bookings')
    return render(request, 'booking/update.html', {
        'form': form, 'title': 'Bookings', 'subTitle': 'Update Booking Details', 'iconClass': 'fa-clipboard-list'
    })


@permission_required('app.add_booking')
def create_client_booking(request):
    customer = get_customer_of_user(request)
    location = get_location_of_user(request)
    form = CreateClientBookingForm(request.POST or None, instance=Booking(create=request.user, customer=customer, location=location, token=_get_token_no(customer, location), schedule_date=now()))

    form.fields['service'].choices = _get_service_of_customer(customer)
    form.fields['client'].queryset = Client.objects.filter(customer=customer)
    if form.is_valid():
        booking = form.save()
        requested_services = request.POST.getlist('service')
        for service in Service.objects.filter(service_id__in=requested_services):
            ServiceBooking.objects.create(booking=booking, service=service)
        messages.success(request, "Your Booking {} has been made for {} service(s)".format(booking.token, len(requested_services)))
        return redirect('create_client_booking')
    return render(request, 'booking/create_client_booking.html', {
        'bookings': Booking.objects.filter(customer=customer, schedule_employee=None, schedule_date=now()),
        'form': form, 'title': 'Client Bookings', 'subTitle': 'Create New Client Booking', 'iconClass': 'fa-clipboard-list'
    })


@permission_required('app.view_bookings')
def view_pending_booking_list(request):
    customer = get_customer_of_user(request)
    location = get_location_of_user(request)
    return render(request, 'booking/pending_list.html', {
        'bookings': Booking.objects.filter(customer=customer, schedule_end_datetime=None, location=location, schedule_date=now()), 'title': 'Bookings', 'subTitle': 'Pending Booking List', 'iconClass': 'fa-clipboard-list'
    })


def _get_service_of_customer(customer):
    opt_groups = []
    service_categories = ServiceCategory.objects.filter(customer=customer)
    for service_category in service_categories:
        services_of_service_category = Service.objects.filter(service_category=service_category)
        services = []
        for service in services_of_service_category:
            services.append((service.service_id, service.service_name))
        opt_groups.append((service_category.service_category_name, services))
    return opt_groups


def _get_token_no(customer, location):
    count = Booking.objects.filter(customer=customer, location=location, schedule_date=now()).count()
    return "TKN{}{}".format(location.location_code, count + 1)


def get_bookings(request):
    customer = get_customer_of_user(request)
    client_id = request.GET.get('client_id', None)
    data = serialize('json', Booking.objects.filter(customer=customer, client_id=client_id))
    return JsonResponse(data, safe=False)
