from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Company


# Create your views here.

def home(request):
    return render(request, 'home.html')


def dashboard(request):
    user = request.user
    if user:
        company = Company.objects.get(id=user.id)
        data = {
            'jobs': company.jobvacancy_set.all()
        }

    return render(request, 'dashboard.html', data)


def login(request):
    if request.method == 'POST':
        data = request.POST
        if User.objects.filter(username=data['username']).exists():
            user = auth.authenticate(username=data['username'], password=data['password'])
            if user is not None:
                auth.login(request, user)
                return redirect('home')

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        data = request.POST
        new_company = Company.objects.create_user(username=data['username'], password=data['password'])
        new_company.save()
        print("Post com sucesso")
        return redirect('login')
    else:
        return render(request, 'register.html')
