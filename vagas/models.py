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


class Company(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=16)


class Candidate(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=16)
    desired_salary = models.ForeignKey(SalaryRange, on_delete=models.CASCADE, default=1)
    experience = models.TextField()
    education_level = models.ForeignKey(EducationLevel, on_delete=models.CASCADE, default=1)


class JobVacancy(models.Model):
    name = models.CharField(max_length=100)
    salary_range = models.ForeignKey(SalaryRange, on_delete=models.CASCADE, default=1)
    requirements = models.TextField(null=True)
    minimum_education = models.ForeignKey(EducationLevel, on_delete=models.CASCADE, default=1)
