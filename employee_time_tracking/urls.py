from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.views import serve
from django.views.generic import TemplateView
from . import views
from .views import login_view, index

urlpatterns = [
    path('static/<path:path>', serve),
    # path('', views.index, name='index'),
    path('register/', views.register_employee, name='register_employee'),
    path('success/', views.success, name='success'),
    # path('add_work_time/', views.add_work_time, name='add_work_time'),
    # path('pages/', views.work_time_success, name='work_time_success'),
    path('login/', login_view, name='login'),
    path('index/', index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    # path('add_time_entry/', views.add_time_entry, name='add_time_entry'),
    # path('time_entries/', views.time_entries, name='time_entries'),
    # path('report/<str:period>/', views.report, name='report'),
    # path('projects/', views.project_list, name='project_list'),
    path('tasks/', views.task_list, name='task_list'),
    path('employee_list/', views.employee_list, name='employee_list'),
    # path('create_project/', views.create_project, name='create_project'),
    path('create_task/', views.create_task, name='create_task'),


    # path('start_timer/', views.start_timer, name='start_timer'),
    # path('pause_timer/', views.pause_timer, name='pause_timer'),
    # path('stop_timer/', views.stop_timer, name='stop_timer'),
    # path('time_entries/', views.time_entries, name='time_entries'),
    # path('report/', views.report, name='report'),
    path('create_project/', views.create_project, name='create_project'),
    path('project_list/', views.project_list, name='project_list'),
    # path('daily_report/', views.daily_report, name='daily_report'),
    # path('weekly_report/', views.weekly_report, name='weekly_report'),
    # path('monthly_report/', views.monthly_report, name='monthly_report'),
    # path('export_csv/', export_csv, name='export_csv'),

    path('report/<str:period>/', views.report, name='report'),
    path('export/<str:period>/', views.ExportCSV.as_view(), name='export_csv'),
]