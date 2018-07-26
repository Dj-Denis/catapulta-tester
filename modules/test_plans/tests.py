from django.test import TestCase, Client
from django.urls import reverse


# Create your tests here.

class PlanCreateTestCase(TestCase):
    fixtures = ['initial_data']

    def setUp(self):
        self.client = Client()

    def test_create_plan(self):
        self.client.logout()
        self.assertTrue(self.client.login(username="test@test.com", password='qwerty12345'))
        response = self.client.post(reverse('plan_create'), {'name': "test name", "description": "test description"})
        self.assertRedirects(response, '/plan/plan_detail/31')

        self.client.logout()
        self.assertTrue(self.client.login(username="noperms@test.com", password='qwerty12345'))
        response = self.client.post(reverse('plan_create'), {'name': "test name", "description": "test description"})
        self.assertRedirects(response, '/accounts/login/?next=/plan/plan_create/')

        self.client.logout()
        self.assertTrue(self.client.login(username="manager@test.com", password='qwerty12345'))
        response = self.client.post(reverse('plan_create'), {'name': "test name", "description": "test description"})
        self.assertRedirects(response, '/plan/plan_detail/32')

