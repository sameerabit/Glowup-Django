from django.contrib import admin


class CustomerGroupAdmin(admin.ModelAdmin):
    list_display = ('group_code', 'group_name')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_group', 'customer_name', 'contact_person', 'contact_email', 'is_active')


class CustomerLocationAdmin(admin.ModelAdmin):
    list_display = ('customer', 'location_name', 'location_code', 'is_active')


class TypeAdmin(admin.ModelAdmin):
    list_display = ('type_description', 'type_category', 'is_active')


class CustomerPaymentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'amount', 'currency')


class CustomerUserGroupAdmin(admin.ModelAdmin):
    list_display = ('group', 'is_eligible')
