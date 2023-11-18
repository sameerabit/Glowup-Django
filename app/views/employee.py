from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from app.forms.employee import CreateEmployeeForm, UpdateEmployeeForm
from app.models import Employee, EmployeeUser, EmployeeService, Service, ServiceCategory, CustomerUser
from config.models import CustomerLocation
from app.utils import get_customer_of_user
from app.check_auth import permission_required
from django.contrib import admin


@permission_required('app.add_employee')
def create_employee(request):
    customer = get_customer_of_user(request)
    form = CreateEmployeeForm(request.POST or None, instance=Employee(create=request.user, customer=customer, employee_code=_get_employee_code(customer)))
    users_of_customer = CustomerUser.objects.filter(customer=customer).exclude(is_salon_admin=True).values('user_id')
    form.fields['location'].queryset = CustomerLocation.objects.filter(customer=customer)
    form.fields['services'].choices = get_service_of_customer(customer)

    if form.is_valid():
        employee = form.save()
        EmployeeUser.objects.create(employee=employee, location=form.cleaned_data['location'])
        for service in Service.objects.filter(service_id__in=request.POST.getlist('services')):
            EmployeeService.objects.create(employee=employee, create=request.user, service=service)
        messages.success(request, 'Employee Created')
        return redirect('view_employees')
    return render(request, 'employee/create.html', {
        'form': form, 'title': 'Employee', 'subTitle': 'Create New Employee', 'iconClass': 'fa-user'
    })


@permission_required('app.view_employees')
def view_employees(request):
    return render(request, 'employee/list.html', {
        'employees': Employee.objects.filter(customer=get_customer_of_user(request)), 'title': 'Employees', 'subTitle': 'List of Employees', 'iconClass': 'fa-user'
    })


@permission_required('app.change_employee')
def update_employee(request, employee_id):
    customer = get_customer_of_user(request)
    employee = get_object_or_404(Employee.objects.filter(customer=customer, employee_id=employee_id))
    employee_user = EmployeeUser.objects.get(employee=employee)
    form = UpdateEmployeeForm(request.POST or None, instance=employee, initial={
        'services': EmployeeService.objects.filter(employee=employee).values_list('service_id', flat=True),
        'location': EmployeeUser.objects.get(employee=employee).location_id
    })
    form.fields['location'].queryset = CustomerLocation.objects.filter(customer=customer)
    form.fields['services'].choices = get_service_of_customer(customer)
    if form.is_valid():
        employee_user.location = form.cleaned_data['location']
        form.save()
        employee_user.save()
        EmployeeService.objects.filter(employee=employee).delete()
        for service in Service.objects.filter(service_id__in=request.POST.getlist('services')):
            EmployeeService.objects.create(employee=employee, create=request.user, service=service)
        messages.success(request, 'Employee Updated')
        return redirect('view_employees')
    return render(request, 'employee/update.html', {
        'form': form, 'title': 'Employee', 'subTitle': 'Update Employee Details', 'iconClass': 'fa-user'
    })


def get_service_of_customer(customer):
    opt_groups = []
    service_categories = ServiceCategory.objects.filter(customer=customer)
    for service_category in service_categories:
        services_of_service_category = Service.objects.filter(service_category=service_category)
        services = []
        for service in services_of_service_category:
            services.append((service.service_id, service.service_name))
        opt_groups.append((service_category.service_category_name, services))
    return opt_groups


def _get_employee_code(customer):
    count = Employee.objects.filter(customer=customer).count()
    return "EMP{}".format(count + 1)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_code', 'first_name', 'last_name', 'customer', 'passcode', 'is_active')


class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ('customer', 'user', 'time_zone', 'location', 'user_type', 'is_salon_admin')
