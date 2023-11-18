from django.shortcuts import render, redirect, get_object_or_404
from app.forms.service import ServiceCreateForm, ServiceUpdateForm, ServiceAssignForm, ServiceDeAllocateForm
from app.models import Service, EmployeeService
from app.check_auth import permission_required


@permission_required('app.add_service')
def create_service(request):
    form = ServiceCreateForm(request.POST or None, instance=Service(create=request.user))
    if form.is_valid():
        form.save()
        return redirect('service_list')
    return render(request, 'services/create.html', {
        'form': form, 'title': 'Services', 'subTitle': 'Create New Service', 'iconClass': 'fa-cogs'
    })


@permission_required('app.view_services')
def view_services(request):
    return render(request, 'services/list.html', {
        'list': Service.objects.all(), 'title': 'Services', 'subTitle': 'List of Services', 'iconClass': 'fa-cogs'
    })


@permission_required('app.change_service')
def update_service(request, id):
    employee = get_object_or_404(Service, service_id=id)
    form = ServiceUpdateForm(request.POST or None, instance=employee)
    if form.is_valid():
        form.save()
        return redirect('service_list')
    return render(request, 'services/update.html', {
        'form': form, 'title': 'Service', 'subTitle': 'Update Service Details', 'iconClass': 'fa-cogs'
    })


def asign_service(request):
    form = ServiceAssignForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('view_allocations')
    return render(request, 'services/asign_employee.html', {
        'form': form, 'title': 'Employee Allocation', 'subTitle': 'Create New Service Category', 'iconClass': 'fa-cogs'
    })


def view_allocations(request):
    return render(request, 'services/assigned_employees_list.html', {
        'list': EmployeeService.objects.all(), 'title': 'Employee Allocation', 'subTitle': 'List of Service Categories', 'iconClass': 'fa-cogs'
    })


def deallocate_service(request, _id):
    alloc = get_object_or_404(EmployeeService, employee_services_id=_id)
    form = ServiceDeAllocateForm(request.POST or None, instance=alloc)
    if form.is_valid():
        form.save()
        return redirect('view_allocations')
    return render(request, 'services/deallocate_employee.html', {
        'form': form, 'title': 'Employee Allocation', 'subTitle': 'Update Service Category Details', 'iconClass': 'fa-cogs'
    })
