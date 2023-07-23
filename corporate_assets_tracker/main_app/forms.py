from django import forms
from .models import Employee, Device

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['company', 'name', 'user_name', 'password', 'role', 'phone']

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'device_type', 'description', 'condition', 'company', 'checked_out_to', 'device_check_out_date', 'device_return_date']
