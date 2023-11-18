from django.urls import path
from django.conf.urls import url
from app.views import views, employee, client, service_category, booking, service, user

urlpatterns = [
    # path('', views.home_page, name='homepage'),
    path('', views.dashboard, name='homepage'),
    path('login/', views.login_view, name="login"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('logout/', views.logout_view, name='logout'),

    path('user/', user.user_registration, name="register"),
    path('users/', user.view_users, name="view_users"),
    url(r'user/(?P<id>\d+)/password/', user.change_password, name="change_password"),
    url(r'^user/(?P<id>\d+)/$', user.user_update, name="update_user"),

    path('employee_allocation/', service.asign_service, name="asign_employee"),
    path('employee_allocations/', service.view_allocations, name="view_allocations"),
    url(r'^employee_allocation/(?P<id>\d+)/$', service.deallocate_service, name="deallocate_employee"),

    path('employee/', employee.create_employee, name="create_employee"),
    path('employees/', employee.view_employees, name="view_employees"),
    url(r'^employee/(?P<employee_id>\d+)/$', employee.update_employee, name="update_employee"),

    path('client/', client.create_client, name="create_client"),
    path('clients/', client.view_clients, name="view_clients"),
    url(r'^client/(?P<client_id>\d+)/$', client.update_client, name="update_client"),
    url(r'^create_client_session/(?P<booking_id>\d+)/$', client.start_client_session, name="create_client_session"),

    path('service_category/', service_category.create_service_category, name="create_service_category"),
    path('service_categories/', service_category.view_service_categories, name="view_service_categories"),
    url(r'^service_category/(?P<service_category_id>\d+)/$', service_category.update_service_category, name="update_service_category"),

    path('client_booking/', booking.create_client_booking, name="create_client_booking"),
    path('client_bookings/', booking.get_bookings, name="get_client_bookings"),
    path('booking/', booking.create_booking, name="create_booking"),
    path('pending_bookings/', booking.view_pending_booking_list, name="view_pending_bookings"),
    path('bookings/', booking.view_bookings, name="view_bookings"),
    url(r'^booking/(?P<booking_id>\d+)/$', booking.update_booking, name="update_booking"),
    url(r'^booking_comment/(?P<booking_id>\d+)/$', client.end_client_session, name="show_booking_comment"),

    path('service', service.create_service, name="service_create"),
    path('services', service.view_services, name="service_list"),
    url(r'^services/(?P<id>\d+)/$', service.update_service, name="service_update"),

]
