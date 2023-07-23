'''
Here there are two main kind of views(Methods).

In the first part few basic fundamentals with a scope for further development.
In the second part views for DRM(Django-Rest-Framework)
'''

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Company, Employee, Device, DeviceLogs
from .serializers import CompanySerializer, EmployeeSerializer, DeviceSerializer, DeviceLogsSerializer
from .forms import EmployeeForm, DeviceForm
from django.utils import timezone
from django.conf import settings

from rest_framework import generics # djangorestframework needs to be installed on the system or env

import stripe # Third party payment gateway. Not available in BD. using it as a placeholder

# Method for the home page of the application
def home(request):
	return render(request, 'home.html')

# (Related to Goal 1) User authentication is a must as manny company with different employees will use this app
def login(request):
    if request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        user = authenticate(request, user_name=user_name, password=password)

        if user is not None:
            if user.is_active:
                # Check if the user is an admin or an employee
                if user.is_superuser:
                    # Admin login
                    login(request, user)
                    return redirect('admin_dashboard')  # Need to create admin_dashboard view
                else:
                    # Employee login
                    login(request, user)
                    return redirect('employee_dashboard')  # Need to create employee_dashboard view
            else:
                # If the user is inactive
                return render(request, 'login.html', {'error_message': 'Your account is inactive.'})
        else:
            # Invalid login credentials
            return render(request, 'login.html', {'error_message': 'Invalid login credentials.'})
    else:
        # Render the login form
        return render(request, 'login.html')

# Method for logging out and redirecting to the homepage. Not necessary to implement as far the project description goes
def logout(request):
	pass

# Methods for adding company employees
def add_company(request):
    if request.method == 'POST':
        name = request.POST['name']
        location = request.POST['location']

        company = Company(name=name, location=location)
        company.save()

        return redirect('companies')

    else:
        return render(request, 'add_company.html')

# (Related to Goal 2) Method for adding employess. Companies can add all of some of it's employees
# Two types of employees (roles) - Admin & User
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_of_employees')  # Need to create this view
    else:
        form = EmployeeForm()

    return render(request, 'add_employee.html', {'form': form})

# (Related to Goal 3) Admins can add devices and assign them to specific employees for a certain period of time
def add_device(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('device_list')  # Need to create this view for viewing device list
    else:
        form = DeviceForm()

    return render(request, 'add_device.html', {'form': form})

# Method for fetching all data from company table in database and show in specific user's end
def list_of_companies(request):
    companies = Company.objects.all()
    return render(request, 'company_list.html', {'companies': companies})

# Method for fetching specific company informations
def company_detail(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    employees = company.employee_set.all()
    return render(request, 'company_detail.html', {'company': company, 'employees': employees})

# Method for fetching all the device lists
def device_list(request):
    devices = Device.objects.all()
    return render(request, 'device_list.html', {'devices': devices})

# (Related to Goal 4) The time of device check in and check out will be available in device details. Company admins can view it.
def device_detail(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    return render(request, 'device_detail.html', {'device': device})

# (Related to Goal 5) Fetch out the device logs information so that admin of company can know the condition of the devices.
def device_logs(request, devicelogs_id):
    device = get_object_or_404(DeviceLogs, id=devicelogs_id)
    return render(request, 'devicelogs.html', {'devicelogs': devicelogs})

# (Bonus Point 3) Third party payment gateway
# API key of stripe. It is not available in Bangladesh.
stripe.api_key = settings.STRIPE_SECRET_KEY

# Model for managing third party strip payment gateway.
def payment(request):
    if request.method == 'POST':
        amount = 1000  # Amount in taka
        try:
            # Create a payment intent
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='bdt',
            )
            return render(request, 'payment.html', {'client_secret': payment_intent.client_secret})
        except stripe.error.CardError as e:
            return render(request, 'payment_error.html', {'error': e.error.message})
    return render(request, 'payment.html')

'''
------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
'''
# Django Rest Framework section


# Manage Company data through API
class CompanyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


# Manage Employees through API. (related Goal 2 & 3)
class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


# Manage Device through API. (related to Goal 4)
class DeviceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


# Manage DeviceLogs through API. (related to Goal 5)
class DeviceLogListCreateAPIView(generics.ListCreateAPIView):
    queryset = DeviceLogs.objects.all()
    serializer_class = DeviceLogsSerializer


class DeviceLogRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeviceLogs.objects.all()
    serializer_class = DeviceLogsSerializer
