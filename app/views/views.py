from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from app.check_auth import authentication_required, allow_anonymous
from app.models import CustomerUser


@authentication_required()
def home_page(request):
    return render(request, 'home/index.html', {
        'title': 'Home', 'subTitle': 'Home Page', 'iconClass': 'fa-home'
    })


@allow_anonymous()
def login_view(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        user = authenticate(**form.cleaned_data)
        login(request, user)
        if user.is_authenticated:
            customer_user = CustomerUser.objects.get(user=user)
            timezone.activate(customer_user.time_zone)
            return redirect('dashboard')
        else:
            logout(request)
    return render(request, 'accounts/login.html', {'form': form})


@authentication_required()
def dashboard(request):
    return render(request, 'home/dashboard.html', {
        'title': 'Dashboard', 'subTitle': 'Everything at a glance', 'iconClass': 'fa-tachometer-alt'
    })


@allow_anonymous()
def logout_view(request):
    timezone.deactivate()
    logout(request)
    return redirect('login')
