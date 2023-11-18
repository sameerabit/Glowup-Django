from django.contrib import admin
from config.models import Customer, CustomerGroup, CustomerPayment, Type, CustomerLocation, CustomerUserGroup
from config import views

# Register your models here.
admin.site.register(Customer, views.CustomerAdmin)
admin.site.register(CustomerGroup, views.CustomerGroupAdmin)
# admin.site.register(CustomerPayment, views.CustomerPaymentAdmin)
admin.site.register(Type, views.TypeAdmin)
admin.site.register(CustomerLocation, views.CustomerLocationAdmin)
admin.site.register(CustomerUserGroup, views.CustomerUserGroupAdmin)
