from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, User
from django.db import models


# Create your models here.
class CustomerManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class Customer(AbstractUser):
    username = None
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomerManager()


class SalaryRange(models.Model):
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description


class EducationLevel(models.Model):
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description


class Candidate(Customer):
    desired_salary = models.FloatField(null=True)
    experience = models.TextField(null=True)
    education_level = models.ForeignKey(EducationLevel, on_delete=models.CASCADE, null=True)


class Company(Customer):
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companys'

    def __str__(self):
        return self.username


class JobVacancy(models.Model):
    title = models.CharField(max_length=100)
    salary_range = models.ForeignKey(SalaryRange, on_delete=models.CASCADE, null=True)
    requirements = models.TextField(null=True)
    minimum_education = models.ForeignKey(EducationLevel, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    candidates = models.ManyToManyField(Candidate, through='Application')
    number_of_candidates = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)


class Application(models.Model):
    job_vacancy = models.ForeignKey(JobVacancy, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    application_date = models.DateField(auto_now_add=True)
