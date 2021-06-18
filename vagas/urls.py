from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/job/detail/<int:id>', views.company_job_detail, name='company_job_detail'),
    path('register/', views.register, name='register'),
    path('job/register', views.job_register, name='job_register'),
    path('job/detail/<int:job_id>', views.job_detail, name='job_detail'),
    path('job/update/<int:id>', views.job_update, name='job_update'),
    path('job/delete/<int:id>', views.job_delete, name='job_delete'),

]
