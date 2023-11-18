from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app.forms.service_category import CreateServiceCategoryForm, UpdateServiceCategoryForm
from app.models import ServiceCategory
from app.utils import get_customer_of_user
from app.check_auth import permission_required


@permission_required('app.add_service_category')
def create_service_category(request):
    form = CreateServiceCategoryForm(request.POST or None, instance=ServiceCategory(create=request.user, customer=get_customer_of_user(request)))
    if form.is_valid():
        form.save()
        messages.success(request, 'Service Category Added.')
        return redirect('view_service_categories')
    return render(request, 'service_category/create.html', {
        'form': form, 'title': 'Service Category', 'subTitle': 'Create New service Category', 'iconClass': 'fa-cogs'
    })


@permission_required('app.view_service_categories')
def view_service_categories(request):
    return render(request, 'service_category/list.html', {
        'service_categories': ServiceCategory.objects.filter(customer=get_customer_of_user(request)), 'title': 'Service Categories', 'subTitle': 'List of Service Categories', 'iconClass': 'fa-cogs'
    })


@permission_required('app.change_service_category')
def update_service_category(request, service_category_id):
    service_category = get_object_or_404(ServiceCategory.objects.filter(customer=get_customer_of_user(request), service_category_id=service_category_id))
    form = UpdateServiceCategoryForm(request.POST or None, instance=service_category)
    if form.is_valid():
        form.save()
        messages.success(request, 'Service Category Updated.')
        return redirect('view_service_categories')
    return render(request, 'service_category/update.html', {
        'form': form, 'title': 'Service Category', 'subTitle': 'Update Service Category Details', 'iconClass': 'fa-cogs'
    })
