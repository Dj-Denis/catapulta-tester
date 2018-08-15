from django.test import TestCase, Client
# Create your tests here.
from django.urls import reverse


class CaseCreateTestCase(TestCase):
    fixtures = ['initial_data']

    def setUp(self):
        self.client = Client()

    def test_create_plan(self):
        self.client.logout()
        self.assertTrue(self.client.login(username="test@test.com", password='qwerty12345'))
        response = self.client.post(reverse('case_create'), {'name': "test name", "excepted_result": "test description"})
        self.assertRedirects(response, '/case/case_detail/51')

        self.client.logout()
        self.assertTrue(self.client.login(username="noperms@test.com", password='qwerty12345'))
        response = self.client.post(reverse('case_create'), {'name': "test name", "excepted_result": "test description"})
        self.assertRedirects(response, '/accounts/login/?next=/case/case_create/')

        self.client.logout()
        self.assertTrue(self.client.login(username="manager@test.com", password='qwerty12345'))
        response = self.client.post(reverse('case_create'), {'name': "test name", "excepted_result": "test description"})
        self.assertRedirects(response, '/case/case_detail/52')

    def test_delete_plan(self):
        self.client.logout()
        self.assertTrue(self.client.login(username="test@test.com", password='qwerty12345'))
        response = self.client.post('/case/case_detail/50', {'submit': True})
