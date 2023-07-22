from django.shortcuts import render

# Method for the home page of the application
def home(request):
	return render(request, 'home.html')
