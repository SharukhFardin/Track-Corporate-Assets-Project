'''
Tests can be performed on all the views. Here I have tried to implement the tests for Company model related API calls only just to my understanding over the testing.
'''

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Company
from .serializers import CompanySerializer,

# Helper function to create test objects
def create_company(name, location):
    return Company.objects.create(name=name, location=location)

# Similaryly the helper functions for creating employee, device and devicelogs can also be coded.


class CompanyTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.company_data = {'name': 'Test Company', 'location': 'Test Location'}
        self.company = create_company(**self.company_data)
        self.url = reverse('company-list')

    # method for testing company info creating
    def test_create_company(self):
        response = self.client.post(self.url, self.company_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) #assertEqual compares two objects and returns a BOOL value
        self.assertEqual(Company.objects.count(), 2)  # One object created in setUp and one from the post request

    def test_update_company(self):
        updated_data = {'name': 'Updated Test Company', 'location': 'Updated Test Location'}
        response = self.client.put(reverse('company-detail', args=[self.company.id]), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.company.refresh_from_db() # Refreshes the database
        self.assertEqual(self.company.name, updated_data['name'])
        self.assertEqual(self.company.location, updated_data['location'])

    def test_delete_company(self):
        response = self.client.delete(reverse('company-detail', args=[self.company.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Company.objects.count(), 0)

# Similarly, you can write tests for Employee, Device, and DeviceLogs views following the same pattern. We can also do tests for every kind of views.
