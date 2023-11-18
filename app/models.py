from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.timezone import now
from config.models import Customer, Type, CustomerLocation


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    registration_no = models.CharField(max_length=100, verbose_name="Registration No", help_text="Enter something unique to client like NIC, Passport No... etc")
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name", null=True, blank=True)
    postal_code = models.CharField(max_length=20, verbose_name="Postal Code")
    email = models.CharField(max_length=100, verbose_name="Email", null=True, blank=True)
    phone_no = models.CharField(max_length=15, verbose_name="Phone No", blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    last_visit_date = models.DateField(null=True, verbose_name="Last Visit Date")
    introduced_by = models.ForeignKey("self", on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="Introduced by")
    is_active = models.BooleanField(default=True, verbose_name="Status")
    create = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Registered by")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Registered on")

    def __str__(self):
        return "{} {} ({})".format(self.first_name, self.last_name, self.registration_no)

    class Meta:
        db_table = 'app_client'
        verbose_name_plural = 'Clients'
        verbose_name = 'Client'
        default_permissions = ()
        permissions = (
            ("add_client", "Can Add Client"),
            ("change_client", "Can Change Client"),
            ("view_clients", "Can View Clients"),
        )


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    employee_code = models.CharField(max_length=10, verbose_name="Employee Code", blank=True, null=True)
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    passcode = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True, verbose_name="Status")
    create = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Registered by")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Registered on")

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        db_table = 'app_employee'
        verbose_name_plural = 'Company Employees'
        verbose_name = 'Employee'
        default_permissions = ()
        unique_together = (('employee_code', 'customer'))
        permissions = (
            ("add_employee", "Can Add Employee"),
            ("change_employee", "Can Change Employee"),
            ("view_employees", "Can View Employees"),
        )


class CustomerUser(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    time_zone = models.CharField(verbose_name="Time Zone", default="UTC", max_length=50)
    location = models.ForeignKey(CustomerLocation, on_delete=models.CASCADE, verbose_name="Location", null=True, blank=False)
    user_type = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="User Type")
    is_salon_admin = models.BooleanField(default=False, verbose_name="Salon Admin")

    def __str__(self):
        return "{} ({}) - {} -[{}]".format(self.user.get_full_name(), self.user.username, self.customer.customer_name, self.location.location_name)

    class Meta:
        db_table = 'app_customer_user'
        verbose_name_plural = 'Company Logins'
        verbose_name = 'Login'
        default_permissions = ()
        permissions = ()


class EmployeeUser(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    location = models.ForeignKey(CustomerLocation, on_delete=models.CASCADE)

    def __str__(self):
        return "{} ({})".format(self.employee.first_name, self.location.location_name)

    class Meta:
        db_table = 'app_employee_user'
        verbose_name_plural = 'Users of Employees'
        default_permissions = ()
        permissions = ()


class ServiceCategory(models.Model):
    service_category_id = models.AutoField(primary_key=True)
    service_category_name = models.CharField(max_length=25, verbose_name="Service Category Name", unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Customer")
    is_active = models.BooleanField(default=True, verbose_name="Status")
    create = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Created by")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Created on")

    def __str__(self):
        return self.service_category_name

    class Meta:
        db_table = 'app_service_category'
        verbose_name_plural = 'Service Categories'
        verbose_name = 'Service Category'
        default_permissions = ()
        permissions = (
            ("add_service_category", "Can Add Service Category"),
            ("change_service_category", "Can Change Service Category"),
            ("view_service_categories", "Can View Service Categories"),
        )


class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=25, verbose_name="Service Name")
    price = models.DecimalField(max_digits=18, decimal_places=3, verbose_name="Price")
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, verbose_name="Service Category")
    is_active = models.BooleanField(default=True, verbose_name="Status")
    create = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Created by")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Created on")

    def __str__(self):
        return self.service_name

    class Meta:
        db_table = 'app_service'
        verbose_name_plural = 'Services'
        verbose_name = 'Service'
        default_permissions = ()
        permissions = (
            ("add_service", "Can Add Service"),
            ("change_service", "Can Change Service"),
            ("view_services", "Can View Services"),
        )


class EmployeeService(models.Model):
    employee_services_id = models.AutoField(primary_key=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Service")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Employee")
    is_active = models.BooleanField(default=True, verbose_name="Status")
    create = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Assigned by")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Assigned on")

    class Meta:
        db_table = 'app_employee_service'
        verbose_name_plural = 'Services of Employees'
        default_permissions = ()
        permissions = ()


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=10, verbose_name="Token No", blank=True, null=True)
    schedule_date = models.DateField(verbose_name="Scheduled Date", blank=True, null=True)
    schedule_time = models.CharField(max_length=25, verbose_name="Scheduled Time", blank=True, null=True)
    client_name = models.CharField(max_length=100, verbose_name="Client Name")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Client")
    phone_no = models.CharField(max_length=15, blank=True, null=True, verbose_name="Phone No")
    client_remark = models.TextField(max_length=250, verbose_name="Comment", null=True, blank=True)
    prefered_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='prefered_employee', related_name="prefered_employee", verbose_name="Prefered Employee", blank=True, null=True)
    status = models.ForeignKey(Type, on_delete=models.CASCADE, db_column='status', verbose_name="Status", blank=True, null=True, limit_choices_to={'is_active': True, 'type_category': 1})
    schedule_remark = models.TextField(max_length=250, blank=True, null=True, verbose_name="Remark")
    schedule_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True, db_column='schedule_employee', related_name="schedule_employee", verbose_name="Scheduled Employee")
    schedule_start_datetime = models.DateTimeField(null=True, blank=True, verbose_name="Session Started on")
    schedule_end_datetime = models.DateTimeField(null=True, blank=True, verbose_name="Session Ended on")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Customer")
    location = models.ForeignKey(CustomerLocation, on_delete=models.CASCADE, verbose_name="Location")
    is_active = models.BooleanField(default=True, verbose_name="Status")
    create = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Created by")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def get_status(self):
        if self.schedule_start_datetime is None:
            return 'start'
        else:
            return 'end'

    class Meta:
        db_table = 'app_booking'
        verbose_name_plural = 'Bookings'
        verbose_name = 'Booking'
        default_permissions = ()
        permissions = (
            ("add_booking", "Can Add Booking"),
            ("change_booking", "Can Change Booking"),
            ("view_bookings", "Can View Bookings"),
            ("add_future_booking", "Can Add Future Booking"),
            ("view_future_bookings", "Can View Future Bookings"),
            ("change_future_booking", "Can Change Future Booking"),
        )


class ServiceBooking(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, verbose_name="Booking")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Service")

    class Meta:
        db_table = 'app_service_booking'
        verbose_name_plural = 'Services of Bookings'
        default_permissions = ()
        permissions = ()


class ClientSession(models.Model):
    client_session_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    personal_style = models.ForeignKey(Type, blank=True, null=True, on_delete=models.CASCADE, db_column='personal_style', related_name="personal_style", verbose_name="Personal Style", limit_choices_to={'is_active': True, 'type_category': 3})
    professional_style = models.ForeignKey(Type, blank=True, null=True, on_delete=models.CASCADE, db_column='professional_style', related_name="professional_style", verbose_name="Professional Style", limit_choices_to={'is_active': True, 'type_category': 4})
    personal_interests = models.CharField(max_length=100, blank=True, null=True, verbose_name="Personal Interests")
    hair_goals = models.ForeignKey(Type, blank=True, null=True, on_delete=models.CASCADE, db_column='hair_goals', related_name="hair_goals", verbose_name="Hair Goals", limit_choices_to={'is_active': True, 'type_category': 5})
    commitment = models.ForeignKey(Type, blank=True, null=True, on_delete=models.CASCADE, db_column='commitment', related_name="commitment", verbose_name="Commitment to Salon Visits", limit_choices_to={'is_active': True, 'type_category': 6})
    time_spending = models.ForeignKey(Type, blank=True, null=True, on_delete=models.CASCADE, db_column='time_spending', related_name="time_spending", verbose_name="Styling time spent at home", limit_choices_to={'is_active': True, 'type_category': 7})
    versality = models.ForeignKey(Type, blank=True, null=True, on_delete=models.CASCADE, db_column='versality', related_name="versality", verbose_name="Versality", limit_choices_to={'is_active': True, 'type_category': 8})
    styling_preferences = models.ForeignKey(Type, blank=True, null=True, on_delete=models.CASCADE, db_column='styling_preferences', related_name="styling_preferences", verbose_name="How you style your hair", limit_choices_to={'is_active': True, 'type_category': 9})
    comfort_level = models.ForeignKey(Type, blank=True, null=True, on_delete=models.CASCADE, db_column='comfort_level', related_name="comfort_level", verbose_name="Styling comfort level", limit_choices_to={'is_active': True, 'type_category': 10})
    preferences = models.CharField(max_length=100, blank=True, null=True, verbose_name="What do you like/dislike about your hair?")
    products = models.CharField(max_length=100, blank=True, null=True, verbose_name="What products are you currently using?")
    abudance = models.ForeignKey(Type, blank=True, null=True, on_delete=models.CASCADE, db_column='abudance', related_name="abudance", verbose_name="Abudance", limit_choices_to={'is_active': True, 'type_category': 11})
    diameter = models.ForeignKey(Type, blank=True, null=True, on_delete=models.CASCADE, db_column='diameter', related_name="diameter", verbose_name="Diameter", limit_choices_to={'is_active': True, 'type_category': 12})
    hair_formation = models.ForeignKey(Type, blank=True, null=True, on_delete=models.CASCADE, db_column='hair_formation', related_name="hair_formation", verbose_name="Hair Formation", limit_choices_to={'is_active': True, 'type_category': 13})
    condition = models.ForeignKey(Type, blank=True, null=True, on_delete=models.CASCADE, db_column='condition', related_name="condition", verbose_name="Condition", limit_choices_to={'is_active': True, 'type_category': 14})
    face_type = models.ForeignKey(Type, blank=True, null=True, on_delete=models.CASCADE, db_column='face_type', related_name="face_type", verbose_name="Face Type", limit_choices_to={'is_active': True, 'type_category': 18})
    distress = models.ForeignKey(Type, blank=True, null=True, on_delete=models.CASCADE, db_column='distress', related_name="distress", verbose_name="Type of Distress", limit_choices_to={'is_active': True, 'type_category': 15})
    skin_tone = models.ForeignKey(Type, blank=True, null=True, on_delete=models.CASCADE, db_column='skin_tone', related_name="skin_tone", verbose_name="Skin Tone", limit_choices_to={'is_active': True, 'type_category': 16})
    chemical_service = models.ForeignKey(Type, blank=True, null=True, on_delete=models.CASCADE, db_column='chemical_service', related_name="chemical_service", verbose_name="Previous Chemical Service", limit_choices_to={'is_active': True, 'type_category': 17})

    class Meta:
        db_table = 'app_client_session'
        verbose_name_plural = 'Client Session'
        default_permissions = ()
        permissions = ()


class SessionImages(models.Model):
    image_id = models.AutoField(primary_key=True)
    client_session = models.ForeignKey(ClientSession, on_delete=models.CASCADE)
    image = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True, verbose_name='Attachments')

    class Meta:
        db_table = 'app_session_image'
        verbose_name_plural = 'Images'
        default_permissions = ()
        permissions = ()
