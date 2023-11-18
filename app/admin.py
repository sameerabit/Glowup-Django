from django.contrib import admin
from app.models import CustomerUser, Employee
from app.views.employee import EmployeeAdmin, CustomerUserAdmin

# Register your models here.
admin.site.register(CustomerUser, CustomerUserAdmin)
admin.site.register(Employee, EmployeeAdmin)
