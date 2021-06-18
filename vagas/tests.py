import datetime

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Count
from django.test import TestCase

# Create your tests here.
from .models import Company, Candidate, JobVacancy
from django.contrib import auth

class LoginTestCase(TestCase):

    company_email = 'company@email.com'
    candidate_email = 'candidate@email.com'
    password = '123'

    def setUp(self) -> None:
        Company.objects.create_user(
            name='Facebook', email=self.company_email, password=self.password
        )
        Candidate.objects.create_user(
            name='Nathan', email=self.candidate_email, password=self.password
        )

    def test_get_first_company(self):
        user = Company.objects.first()
        self.assertIsNotNone(user, 'User is none')

    def test_create_company_without_username(self):
        user = Company.objects.create_user(email='email@email.com', password='123')
        self.assertIsNotNone(user, 'User not created')

    def test_authenticate_company_with_username_fails(self):
        name = 'Facebook'
        user = auth.authenticate(name=name, password=self.password)
        self.assertIsNone(user, 'User should not be authenticated')

    def test_authenticate_company_with_email(self):
        email2 = 'face@email.com.br'
        user = auth.authenticate(email=self.company_email, password=self.password)
        user2 = auth.authenticate(email=email2, password=self.password)

        self.assertIsNotNone(user, 'User should be authenticated')
        self.assertIsNone(user2, 'User should not be authenticated')

    def test_candidate_authenticates_with_username_fails(self):

        candidate = auth.authenticate(email=self.candidate_email, password=self.password)

        self.assertIsNotNone(candidate)


