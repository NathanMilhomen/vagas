from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, User
from django.db import models


# Create your models here.
class SalaryRange(models.Model):
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description


class EducationLevel(models.Model):
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description


class Company(User):

    def __str__(self):
        return self.username


class Candidate(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=16)
    desired_salary = models.ForeignKey(SalaryRange, on_delete=models.CASCADE, default=1)
    experience = models.TextField()
    education_level = models.ForeignKey(EducationLevel, on_delete=models.CASCADE, default=1)


class JobVacancy(models.Model):
    description = models.CharField(max_length=100)
    salary_range = models.ForeignKey(SalaryRange, on_delete=models.CASCADE, default=1)
    requirements = models.TextField(null=True)
    minimum_education = models.ForeignKey(EducationLevel, on_delete=models.CASCADE, default=1)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    number_of_candidates = models.IntegerField(default=0)
