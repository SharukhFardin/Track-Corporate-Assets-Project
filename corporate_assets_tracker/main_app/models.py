from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

# Company Model. It has one-to-many relationship with Employee
class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self): # Python special method for object string representation
    	return self.name


'''
Employee Model. It has one-to-many relationship with Device. It has a foreign key for indicating which company
the employee belongs to.
'''
class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE) # Foreign key to the company the employee belongs to
    name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=20) # Admin and Employee
    phone = models.CharField(max_length=100)

    def __str__(self):
    	return self.name


'''
Device Model. Represents phone,table,laptop e.t.c. Has foreign key to the company it belongs to and from which
employee it was checked out from. It has one-to-many relationship with deviceLogs
'''
class Device(models.Model):
    name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=50) # phone/tablet/laptop
    description = models.TextField()
    condition = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE) # Foreign key to the company it belongs to
    checked_out_to = models.ForeignKey(Employee, related_name='devices_checked_out', on_delete=models.SET_NULL, null=True, blank=True) # Foreign key to the employee it belongs to
    device_check_out_date = models.DateTimeField(null=True, blank=True)
    device_return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
    	return self.name


'''
DeviceLogs Model. It represents the logs of device checkouts and returns. It has foreign key to the device
and the Employee related to each log entry.
'''
class DeviceLogs(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE) # Foreign key to the device this log belongs to
    checked_out_by = models.ForeignKey(Employee, on_delete=models.CASCADE) # Foreign key to the employee the device was checked out from
    checkout_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    checkout_condition = models.TextField()
    return_condition = models.TextField(null=True, blank=True)

    def __str__(self):
    	return f"device name :{self.device.name} - checkout date: {self.checked_out_date} - checkout condition :{self.checkout_condition}"


'''
(Bonus Point 3) Payment Model for integrating payments or subscriptions via a third-party payment gateway (Stripe)
'''
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('success', 'Success'), ('failed', 'Failed')])
