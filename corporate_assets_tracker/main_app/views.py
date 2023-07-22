from django.shortcuts import render, redirect
from .models import Company, Employee, Device, DeviceLogs

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
