from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
	path("", views.home, name='home'),

    # More and more urlpatterns needs to be added here for further development of the project. Not necessary right now as per requirements.

    # API paths
    path('api/companies/', views.CompanyListCreateAPIView.as_view(), name='company-list-create'),
    path('api/companies/<int:pk>/', views.CompanyRetrieveUpdateDestroyAPIView.as_view(), name='company-retrieve-update-destroy'),
    path('api/employees/', views.EmployeeListCreateAPIView.as_view(), name='employee-list-create'),
    path('api/employees/<int:pk>/', views.EmployeeRetrieveUpdateDestroyAPIView.as_view(), name='employee-retrieve-update-destroy'),
    path('api/devices/', views.DeviceListCreateAPIView.as_view(), name='device-list-create'),
    path('api/devices/<int:pk>/', views.DeviceRetrieveUpdateDestroyAPIView.as_view(), name='device-retrieve-update-destroy'),
    path('api/device-logs/', views.DeviceLogListCreateAPIView.as_view(), name='device-log-list-create'),
    path('api/device-logs/<int:pk>/', views.DeviceLogRetrieveUpdateDestroyAPIView.as_view(), name='device-log-retrieve-update-destroy'),

]
