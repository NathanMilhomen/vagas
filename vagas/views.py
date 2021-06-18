import datetime

from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.shortcuts import render, redirect

from .models import Company, SalaryRange, JobVacancy, EducationLevel, Candidate, Customer, Application


# Create your views here.

def home(request):
    context = {
        'jobs': JobVacancy.objects.all()
    }
    return render(request, 'home.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    elif request.method == 'POST':
        data = request.POST
        if Customer.objects.filter(email=data['email']).exists():
            user = auth.authenticate(email=data['email'], password=data['password'])
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')

    return render(request, 'login.html')


@login_required
def logout(request):
    auth.logout(request)

    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    company = Company.objects.get(id=user.id)
    job_vacancy_per_month = []
    candidates_per_month = []

    jobs = company.jobvacancy_set.all()

    for month in range(1, 13):
        filtered_job = jobs.filter(created_at__month=month, created_at__year=int(datetime.datetime.now().year))
        candidates = 0
        for f_job in filtered_job:
            candidates += f_job.application_set.filter(
                application_date__month=month,
                application_date__year=int(datetime.datetime.now().year)).count()

        candidates_per_month.append(candidates)
        job_vacancy_per_month.append(filtered_job.count())

    data = {
        'jobs': jobs,
        'months': ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
        'numbers_of_vacancy': job_vacancy_per_month,
        'numbers_of_candidates': candidates_per_month
    }

    return render(request, 'dashboard.html', data)


def register(request):
    if request.method == 'POST':
        data = request.POST
        new_company = Company.objects.create_user(email=data['email'], password=data['password'], name=data['name'])
        new_company.save()
        return redirect('login')
    else:
        return render(request, 'register.html')


salaries = []
educations = []


@login_required
def job_register(request):
    global salaries, educations
    # TODO: Olhar django forms
    # TODO: Tentar fazer com cache
    if not salaries or not educations:
        salaries = SalaryRange.objects.all()
        educations = EducationLevel.objects.all()

    if request.method == 'POST':
        data = request.POST

        salary_index = int(data['salary_range'])
        education_index = int(data['education'])
        company = Company.objects.get(pk=request.user.id)
        JobVacancy.objects.update_or_create(
            id=data['id'] if data['id'] != '' else None,
            defaults={
                'title': data['title'],
                'salary_range': salaries[salary_index],
                'minimum_education': educations[education_index],
                'requirements': data['requirements'],
                'company': company
            }

        )

        return redirect('dashboard')

    context = {
        'salaries': enumerate(salaries),
        'educations': enumerate(educations)
    }
    return render(request, 'job_register.html', context)


@login_required
def job_detail(request, job_id: int):
    global educations
    candidate_exists = None
    job = JobVacancy.objects.get(pk=job_id)

    if not educations:
        educations = EducationLevel.objects.all()

    # Candidatar usuário
    if request.method == 'POST':
        data = request.POST

        education_index = int(data['education'])
        candidate_exists = Customer.objects.filter(email=data['email']).exists()

        if not candidate_exists:
            new_candidate = Candidate.objects.create(
                name=data['name'],
                email=data['email'],
                experience=data['experience'],
                education_level=educations[education_index],
                desired_salary=data['salary']
            )

            job.number_of_candidates += 1
            job.save()
            Application.objects.create(job_vacancy=job, candidate=new_candidate).save()

            return redirect('home')

    context = {
        'job': job,
        'educations': enumerate(educations),
        'created': not candidate_exists
    }
    return render(request, 'candidate_job_detail.html', context)


@login_required
def company_job_detail(request, id):
    job = JobVacancy.objects.get(pk=id)

    context = {
        'job': job,
        'candidates': job.candidates.all()
    }
    return render(request, 'company_job_detail.html', context)


@login_required
def job_update(request, id):
    global educations, salaries

    if not salaries or not educations:
        salaries = SalaryRange.objects.all()
        educations = EducationLevel.objects.all()

    job = JobVacancy.objects.get(pk=id)
    context = {
        'job': job,
        'candidates': job.candidates.all(),
        'salaries': enumerate(salaries),
        'educations': enumerate(educations)
    }
    return render(request, 'job_register.html', context)


@login_required
def job_delete(request, id):
    job = JobVacancy.objects.get(pk=id)
    job.delete()
    return redirect('dashboard')
