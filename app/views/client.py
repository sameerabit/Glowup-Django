from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now
from django.utils import formats
from app.forms.client import CreateClientForm, UpdateClientForm, ClientSessionStartForm, ClientSessionEndForm
from app.forms.booking import ViewClientBookingForm
from app.models import Client, Booking, ClientSession, Employee, ServiceBooking, Service, SessionImages
from app.utils import get_customer_of_user
from app.check_auth import permission_required


@permission_required('app.add_client')
def create_client(request):
    form = CreateClientForm(request.POST or None, instance=Client(create=request.user, customer=get_customer_of_user(request)))
    if form.is_valid():
        form.save()
        return redirect('view_clients')
    return render(request, 'client/create.html', {
        'form': form, 'title': 'Client', 'subTitle': 'Create New Client', 'iconClass': 'fa-user-tie'
    })


@permission_required('app.view_clients')
def view_clients(request):
    return render(request, 'client/list.html', {
        'clients': Client.objects.filter(customer=get_customer_of_user(request)), 'title': 'Clients',
        'subTitle': 'List of Clients', 'iconClass': 'fa-user-tie'
    })


@permission_required('app.change_client')
def update_client(request, client_id):
    client = get_object_or_404(Client.objects.filter(customer=get_customer_of_user(request), client_id=client_id))
    form = UpdateClientForm(request.POST or None, instance=client)
    if form.is_valid():
        form.save()
        return redirect('view_clients')
    return render(request, 'client/update.html', {
        'form': form, 'title': 'Client', 'subTitle': 'Update Client Details',
        'iconClass': 'fa-user-tie'
    })


def start_client_session(request, booking_id):
    customer = get_customer_of_user(request)
    booking = get_object_or_404(Booking.objects.filter(customer=customer, booking_id=booking_id))
    history = ClientSession.objects.exclude(booking__client=None).filter(booking__client=booking.client).order_by('client_session_id').reverse()
    instance = ClientSession(booking=booking)
    if history.count() > 0:
        last_one = history[0]
        instance.personal_style = last_one.personal_style
        instance.professional_style = last_one.professional_style
        instance.personal_interests = last_one.personal_interests
        instance.hair_goals = last_one.hair_goals
        instance.commitment = last_one.commitment
        instance.time_spending = last_one.time_spending
        instance.versality = last_one.versality
        instance.styling_preferences = last_one.styling_preferences
        instance.comfort_level = last_one.comfort_level
        instance.preferences = last_one.preferences
        instance.products = last_one.products
        instance.abudance = last_one.abudance
        instance.diameter = last_one.diameter
        instance.hair_formation = last_one.hair_formation
        instance.condition = last_one.condition
        instance.face_type = last_one.face_type
        instance.distress = last_one.distress
        instance.skin_tone = last_one.skin_tone
        instance.chemical_service = last_one.chemical_service

    form = ClientSessionStartForm(request.POST or None, instance=instance)
    booking_form = ViewClientBookingForm(instance=booking, initial={
        'service': ServiceBooking.objects.filter(booking=booking).values_list('service_id', flat=True)
    })
    if form.is_valid():
        entered_employee = form.cleaned_data['employee_id']
        employee = Employee.objects.filter(customer=customer, passcode=form.cleaned_data['passcode'], employee_id=entered_employee.employee_id).first()
        if employee is None:
            messages.error(request, "Incorrect passcode provided")
        else:
            booking.schedule_remark = form.cleaned_data['schedule_remark']
            booking.schedule_time = formats.time_format(now())
            booking.schedule_employee = employee
            booking.schedule_start_datetime = now()
            booking.save()
            form.save()
            messages.success(request, "{} is marked as started by {}".format(booking.token, employee.first_name))
        return render(request, 'client/popup_closed.html')
    return render(request, 'client/start_client_session.html', {
        'booking_form': booking_form, 'form': form,
        'title': 'Client Session', 'subTitle': 'Create Client Session', 'iconClass': 'fa-clipboard-list'
    })


def end_client_session(request, booking_id):
    customer = get_customer_of_user(request)
    booking = get_object_or_404(Booking.objects.filter(booking_id=booking_id, customer=customer))
    client_session = get_object_or_404(ClientSession.objects.filter(booking_id=booking_id))
    form = ClientSessionEndForm(request.POST or None, instance=booking, initial={
        'todo_type': booking.get_status(),
        'services': ServiceBooking.objects.filter(booking=booking).values_list('service_id', flat=True)
    })
    attachments = request.FILES.getlist('attachments')

    if form.is_valid():
        employee = Employee.objects.filter(customer=customer, passcode=form.cleaned_data['passcode'], employee_id=booking.schedule_employee.employee_id).first()

        if employee is None:
            messages.error(request, "Incorrect passcode provided")
        else:
            # delete existing service bookings
            ServiceBooking.objects.filter(booking=booking).delete()

            # save service bookings
            for service in Service.objects.filter(service_id__in=request.POST.getlist('services')):
                ServiceBooking.objects.create(booking=booking, service=service)

            # save images
            for attachment in attachments:
                SessionImages.objects.create(client_session=client_session, image=attachment)

            # set time
            booking.schedule_end_datetime = now()
            messages.success(request, "{} is marked as ended by {}".format(booking.token, employee.first_name))
            booking.save()
        if form.cleaned_data['register_as_new']:
            return redirect('create_client')
        else:
            return render(request, 'client/popup_closed.html')
    return render(request, 'client/end_client_session.html', {
        'form': form, 'title': 'Bookings', 'subTitle': 'Update Booking Comment', 'iconClass': 'fa-clipboard-list'
    })
