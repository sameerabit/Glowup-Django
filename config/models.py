from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.timezone import now

type_categorizations = (
    (1, 'Status'),
    (2, 'Booking Type'),
    (3, 'Personal Style'),
    (4, 'Professional Style'),
    (5, 'Hair Goals'),
    (6, 'Commitment to Salon Visits'),
    (7, 'Styling Time'),
    (8, 'Versality'),
    (9, 'How you Style'),
    (10, 'Styling Comfort Level'),
    (11, 'Abudance'),
    (12, 'Diameter'),
    (13, 'Hair Formation'),
    (14, 'Condition'),
    (15, 'Type of Distress'),
    (16, 'Skin Tone'),
    (17, 'Previous Chemical Service'),
    (18, 'Face Type')
)


class CustomerGroup(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_code = models.CharField(max_length=25, verbose_name="Group Code", unique=True)
    group_name = models.CharField(max_length=50, verbose_name="Group Name")

    def __str__(self):
        return self.group_name

    class Meta:
        db_table = 'config_customer_group'
        verbose_name_plural = 'Company Groups'
        verbose_name = 'Company Group'
        default_permissions = ()
        permissions = (
            ("add_customer_group", "Can Add Customer Group"),
            ("change_customer_group", "Can Change Customer Group"),
            ("view_customer_groups", "Can View Customer Groups"),
        )


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_group = models.ForeignKey(CustomerGroup, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100, verbose_name="Company Name", blank=True)
    contact_person = models.CharField(max_length=100, verbose_name="Contact Person", blank=True)
    address_1 = models.CharField(max_length=100, verbose_name="Address Line 1", blank=True)
    address_2 = models.CharField(max_length=100, verbose_name="Address Line 2", blank=True)
    city = models.CharField(max_length=50, verbose_name="City", blank=True)
    postal_code = models.CharField(max_length=20, verbose_name="Postal Code", blank=True)
    country = models.CharField(max_length=25, verbose_name="Country", blank=True)
    currency = models.CharField(max_length=10, verbose_name="Currency", blank=True)
    contact_land = models.CharField(max_length=15, verbose_name="Telephone", blank=True)
    contact_mobile = models.CharField(max_length=15, verbose_name="Mobile", blank=True)
    contact_email = models.EmailField(max_length=100, verbose_name="Email", blank=True)
    admin_email = models.EmailField(max_length=100, verbose_name="Admin Email")
    is_active = models.BooleanField(default=True, verbose_name="Status")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Registered on")
    create = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Registered by")

    def __str__(self):
        return self.customer_name

    class Meta:
        db_table = 'config_customer'
        verbose_name_plural = 'Companies'
        verbose_name = 'Company'
        default_permissions = ()
        permissions = (
            ("add_customer", "Can Add Customer"),
            ("change_customer", "Can Change Customer"),
            ("view_customers", "Can View Customers"),
        )


class CustomerLocation(models.Model):
    location_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    location_name = models.CharField(max_length=50, verbose_name="Location")
    location_code = models.CharField(max_length=3, verbose_name="Location Code")
    address_1 = models.CharField(max_length=100, verbose_name="Address Line 1", blank=True)
    address_2 = models.CharField(max_length=100, verbose_name="Address Line 2", blank=True)
    city = models.CharField(max_length=25, verbose_name="City", blank=True)
    contact_mobile = models.CharField(max_length=15, verbose_name="Mobile", blank=True)
    contact_land = models.CharField(max_length=15, verbose_name="Telephone", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Status")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Registered on")
    create = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Registered by")

    def __str__(self):
        return self.location_name

    class Meta:
        db_table = 'config_customer_location'
        verbose_name_plural = 'Company Locations'
        verbose_name = 'Location'
        default_permissions = ()
        permissions = (
            ("add_customer_location", "Can Add Customer Location"),
            ("change_customer_location", "Can Change Customer Location"),
            ("view_customer_locations", "Can View Customer Locations"),
        )


class CustomerPayment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Amount")
    currency = models.CharField(max_length=10, verbose_name="Currency")
    due_date = models.DateField(verbose_name="Due Date")
    expiry_date = models.DateField(verbose_name="Expiry Date")
    payment_method = models.CharField(max_length=10, verbose_name="Payment Method")
    payment_ref = models.CharField(max_length=25, verbose_name="Reference No")
    payment_done = models.BooleanField(default=True, verbose_name="Payment OK")
    create = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Collected by")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Collected on")

    class Meta:
        db_table = 'config_customer_payment'
        verbose_name_plural = 'Customer Payments'
        default_permissions = ()
        permissions = (
            ("add_customer_payment", "Can Add Customer Payment"),
            ("change_customer_payment", "Can Change Customer Payment"),
            ("view_customer_payments", "Can View Customer Payments"),
        )


class Type(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_description = models.CharField(max_length=50, verbose_name="Type Description")
    type_category = models.IntegerField(verbose_name="Type Categorization", choices=type_categorizations)
    is_active = models.BooleanField(default=True, verbose_name="Status")

    def __str__(self):
        return self.type_description

    class Meta:
        db_table = 'config_type'
        verbose_name_plural = 'Type'
        verbose_name = 'Type'
        default_permissions = ()
        unique_together = (('type_description', 'type_category'))
        permissions = (
            ("add_config_type", "Can Add Config Type"),
            ("change_config_type", "Can Change Config Type"),
            ("view_config_types", "Can View Config Types"),
        )


class CustomerUserGroup(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, unique=True)
    is_eligible = models.BooleanField(default=False, verbose_name="Eligible", help_text="Can Customer assign this Type to a Employee?")

    def __str__(self):
        return '{} is eligible'.format(self.group.name)

    class Meta:
        db_table = 'config_customer_user_group'
        verbose_name_plural = 'User Group Eligibility of Customers'
        default_permissions = ()
        permissions = (
            ("add_customer_user_group", "Can Add User Group Eligibility of Customer"),
            ("change_customer_user_group", "Can Change User Group Eligibility of Customer"),
            ("view_customer_user_groups", "Can View User Group Eligibility of Customers"),
        )
