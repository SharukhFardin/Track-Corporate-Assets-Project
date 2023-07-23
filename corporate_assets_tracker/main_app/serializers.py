'''
Serializers classes in Django rest framework allows us to convert
django model instances into python datatypes, mostly json.
'''

from rest_framework import serializers
from .models import Company, Employee, Device, DeviceLogs

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__' # includes all fields from the models

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class DeviceLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceLogs
        fields = '__all__'
