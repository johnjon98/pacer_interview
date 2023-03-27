from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from main.models import User
from main.management.commands.loaddata import Command
import io 
import sys
class SimpleTest(APITestCase):
    def setUp(self):
        # create a text trap and redirect stdout
        text_trap = io.StringIO()
        sys.stdout = text_trap

        c = Command()
        c.handle()
        self.admin_user = User.objects.get(email='1234@admin.com')

        # now restore stdout function
        sys.stdout = sys.__stdout__

    def test_admin_user_exists(self):
        self.assertEqual(User.objects.filter(email='1234@superuser.com').exists(), True)
        self.assertEqual(User.objects.filter(email='1234@admin.com').exists(), True)
        print('1. test_admin_user_exists passed')

    def test_get_score(self):
        """
        Ensure our get_score API is running as expected
        """
        user = self.admin_user
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/get_score/?input={input}'.format(input='80'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Score'], 81)
        print('2. test_get_score passed')