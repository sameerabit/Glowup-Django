from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from app.forms.user import CreateUserForm, UpdateUserForm, ChangePasswordForm
from app.models import CustomerUser
from config.models import CustomerLocation, CustomerUserGroup
from app.utils import get_customer_of_user
from app.check_auth import permission_required


@permission_required('auth.add_user')
def user_registration(request):
    form = CreateUserForm(request.POST or None)
    customer = get_customer_of_user(request)
    form.fields['location'].queryset = CustomerLocation.objects.filter(customer=customer)
    form.fields['user_type'].queryset = Group.objects.filter(id__in=CustomerUserGroup.objects.filter(is_eligible=True).values('id'))
    if form.is_valid():
        user = form.save()
        customer = get_customer_of_user(request)
        CustomerUser.objects.create(customer=customer, user=user, location=form.cleaned_data['location'], user_type=form.cleaned_data['user_type'], time_zone=form.cleaned_data['time_zone'])
        return redirect('view_users')
    return render(request, 'user/create.html', {'form': form, 'title': 'Users', 'subTitle': 'Create User', 'iconClass': 'fa-users'})


@permission_required('auth.change_user')
def user_update(request, id):
    customer = get_customer_of_user(request)
    user_ids = CustomerUser.objects.filter(customer=customer).values('user_id')
    user = get_object_or_404(User.objects.filter(id__in=user_ids, id=id))
    customer_user = CustomerUser.objects.get(customer=customer, user=user)
    form = UpdateUserForm(request.POST or None, instance=user, initial={
        'location': customer_user.location_id,
        'user_type': customer_user.user_type_id,
        'time_zone': customer_user.time_zone
    })
    form.fields['location'].queryset = CustomerLocation.objects.filter(customer=customer)
    form.fields['user_type'].queryset = Group.objects.filter(id__in=CustomerUserGroup.objects.filter(is_eligible=True).values('id'))
    if form.is_valid():
        form.save()

        # delete existing customer user
        CustomerUser.objects.filter(customer=customer, user=user).delete()
        CustomerUser.objects.create(customer=customer, user=user, location=form.cleaned_data['location'], user_type=form.cleaned_data['user_type'], time_zone=form.cleaned_data['time_zone'])
        
        return redirect('view_users')
    return render(request, 'user/update.html', {
        'form': form, 'title': 'Users', 'subTitle': 'Update User Details', 'iconClass': 'fa-users'
    })


@permission_required('auth.view_user')
def view_users(request):
    customer = get_customer_of_user(request)
    print(customer, "Customer ID is", customer.customer_id)
    user_ids = CustomerUser.objects.filter(customer=customer).values('user_id')
    return render(request, 'user/list.html', {
        'users': User.objects.filter(id__in=user_ids), 'title': 'Users', 'subTitle': 'List of Users', 'iconClass': 'fa-users'
    })


@permission_required('auth.change_user')
def change_password(request, id):
    customer = get_customer_of_user(request)
    user_ids = CustomerUser.objects.filter(customer=customer).values('user_id')
    user = get_object_or_404(User.objects.filter(id__in=user_ids, id=id))
    form = ChangePasswordForm(request.POST or user)
    if form.is_valid():
        form.save()
        return redirect('view_users')
    return render(request, 'user/change_password.html', {'form': form, 'title': 'Users', 'subTitle': 'Create User', 'iconClass': 'fa-users'})
