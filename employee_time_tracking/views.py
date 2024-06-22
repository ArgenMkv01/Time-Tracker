from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Project, Task, WorkTime, WorkSession
from .forms import EmployeeRegistrationForm, ProjectForm, TaskForm
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
import csv
from django.views.generic import View


def login_view(request):
    error_message = None
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Перенаправление на главную страницу после успешного входа
            else:
                error_message = 'Invalid username or password'
        else:
            error_message = 'Invalid username or password'
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form, 'error_message': error_message})


def index(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        employee = Employee.objects.first()  # упрощенно, берем первого сотрудника

        if employee:
            if action == 'start':
                WorkSession.objects.create(employee=employee, start_time=timezone.now())
            elif action == 'pause' or action == 'stop':
                session = WorkSession.objects.filter(employee=employee, end_time__isnull=True).last()
                if session:
                    session.end_time = timezone.now()
                    session.total_time = session.end_time - session.start_time
                    session.save()

        return redirect('index')

    return render(request, 'index.html')    


class ExportCSV(View):
    def get(self, request, period):
        if period == 'день':
            start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'неделю':
            start_date = timezone.now() - timedelta(days=timezone.now().weekday())
        elif period == 'месяц':
            start_date = timezone.now().replace(day=1)
        else:
            return HttpResponse(status=400)

        end_date = timezone.now()
        sessions = WorkSession.objects.filter(start_time__range=(start_date, end_date))

        if period == 'день':
            fileName = 'dayly'
        elif period == 'неделю':
            fileName = 'weekly'
        elif period == 'месяц':
            fileName = 'monthly'
        else:
            fileName = ''
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{fileName}_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Employee', 'Start Time', 'End Time', 'Total Time'])

        for session in sessions:
            writer.writerow([session.employee, session.start_time, session.end_time, session.total_time])

        return response

def report(request, period):
    employee = Employee.objects.first()  # Упрощенно, берем первого сотрудника
    now = timezone.now()

    if period == 'день':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == 'неделю':
        start_date = now - timedelta(days=now.weekday())
    elif period == 'месяц':
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Фильтруем сессии по сотруднику и дате начала
    sessions = WorkSession.objects.filter(employee=employee, start_time__gte=start_date)

    # Вычисляем общее отработанное время за выбранный период
    total_time = sum((session.total_time for session in sessions), timedelta())

    # Форматируем общее отработанное время в строку без долей секунд
    total_time_formatted = str(total_time).split('.')[0]

    return render(request, 'report.html', {
        'sessions': sessions,
        'total_time': total_time_formatted,
        'period': period.capitalize(),  # Делаем первую букву заглавной для корректного отображения периода
    })


def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

def register_employee(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.user = request.user
            employee.save()
            return redirect('success')
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'register_employee.html', {'form': form})

def success(request):
    return render(request, 'success.html')


def logout_view(request):
    logout(request)
    return redirect('login')

