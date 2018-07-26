from django.test import Client
from django.test import TestCase


# Create your tests here.

class AccountTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        self.urls = (
            ('/account/accounts_list/', '/accounts/login/?next=/account/accounts_list/'),
            ('/account/account_edit/1', '/accounts/login/?next=/account/account_edit/1'),
            ('/account/account_add/', '/accounts/login/?next=/account/account_add/'),
            ('/account/account_delete/1', '/accounts/login/?next=/account/account_delete/1'),
            ('/account/groups_list/', '/accounts/login/?next=/account/groups_list/'),
            ('/account/group_create/', '/accounts/login/?next=/account/group_create/'),
            ('/account/group_edit/1', '/accounts/login/?next=/account/group_edit/1'),
            ('/account/group_delete/1', '/accounts/login/?next=/account/group_delete/1')
        )

    def test_noLogin(self):

        for url in self.urls:
            response = self.c.get(url[0])
            self.assertRedirects(response, url[1])

