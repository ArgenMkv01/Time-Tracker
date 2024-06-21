from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Project, Task, WorkTime, WorkSession
from .forms import EmployeeRegistrationForm, ProjectForm, TaskForm, LoginForm, WorkTimeForm
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
import csv
from django.views.generic import View

import secrets

def generate_secret_key():
    return secrets.token_hex(50)  

print(generate_secret_key())



# def export_csv(request):
#     worktimes = WorkTime.objects.filter(user=request.user)
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="daily_report.csv"'

#     writer = csv.writer(response)
#     writer.writerow(['Start Time', 'End Time', 'Duration'])
#     for worktime in worktimes:
#         writer.writerow([worktime.start_time, worktime.end_time, worktime.duration])

#     return response

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

# def home(request):
#     return render(request, 'index.html')


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


            # @login_required
            # def index(request):
            #     # Логика для отображения главной страницы
            #     return render(request, 'index.html', {'username': request.user.username})

            # def start_timer(request):
            #     # Логика для старта таймера
            #     if request.method == 'POST':
            #         # Создаем новую запись WorkTime при старте таймера
            #         WorkTime.objects.create(user=request.user, start_time=timezone.now())
            #         return redirect('index')
            #     return render(request, 'index.html')

            # def pause_timer(request):
            #     # Логика для паузы таймера
            #     if request.method == 'POST':
            #         # Находим последнюю запись WorkTime для текущего пользователя и приостанавливаем таймер
            #         last_worktime = WorkTime.objects.filter(user=request.user).latest('start_time')
            #         last_worktime.pause_time = timezone.now()
            #         last_worktime.save()
            #         return redirect('index')
            #     return render(request, 'index.html')

            # def stop_timer(request):
            #     # Логика для остановки таймера и сохранения времени
            #     if request.method == 'POST':
            #         # Находим последнюю запись WorkTime для текущего пользователя и останавливаем таймер
            #         last_worktime = WorkTime.objects.filter(user=request.user).latest('start_time')
            #         last_worktime.end_time = timezone.now()
            #         # Вычисляем отработанное время
            #         last_worktime.worked_hours = (last_worktime.end_time - last_worktime.start_time).total_seconds() / 3600
            #         last_worktime.save()
            #         return redirect('index')
            #     return render(request, 'index.html')

            # # def index(request):
            # #     return render(request, 'index.html')

            # def save_time(request):
            #     if request.method == 'POST':
            #         # Получить время от фронтенда
            #         time = request.POST.get('time')
            #         # Сохранить время в базе данных
            #         worktime = WorkTime.objects.create(start_time=timezone.now(), worked_hours=time)
            #         return JsonResponse({'message': 'Время успешно сохранено в БД'})
            #     return JsonResponse({'message': 'Метод не разрешен'}, status=405)

            # def daily_report(request):
            #     # Получаем все записи WorkTime для текущего пользователя
            #     worktimes = WorkTime.objects.filter(user=request.user)
            #     return render(request, 'daily_report.html', {'worktimes': worktimes})


                    # def weekly_report(request):
                    #     # Получаем текущую дату
                    #     today = datetime.now()
                    #     # Вычисляем начало недели (понедельник)
                    #     start_of_week = today - timedelta(days=today.weekday())
                    #     # Вычисляем конец недели (воскресенье)
                    #     end_of_week = start_of_week + timedelta(days=6)
                    #     # Фильтруем данные за текущую неделю
                    #     worktimes = WorkTime.objects.filter(start_time_gte=start_of_week, start_time_lte=end_of_week)
                    #     # Считаем общее количество отработанных часов
                    #     total_hours_worked = sum((work.end_time - work.start_time).total_seconds() / 3600 for work in worktimes)
                    #     context = {
                    #         'worktimes': worktimes,
                    #         'start_of_week': start_of_week,
                    #         'end_of_week': end_of_week,
                    #         'total_hours_worked': total_hours_worked,
                    #     }
                    #     return render(request, 'weekly_report.html', context)

                    # def monthly_report(request):
                    #     today = timezone.now().date()
                    #     start_of_month = today.replace(day=1)
                    #     end_of_month = start_of_month.replace(month=start_of_month.month % 12 + 1, day=1) - timedelta(days=1)
                    #     worktimes = WorkTime.objects.filter(start_time_date_range=[start_of_month, end_of_month])
                    #     total_time_worked = timedelta()

                    #     # Суммируем время отработки всех сотрудников
                    #     for worktime in worktimes:
                    #         if worktime.start_time and worktime.end_time:
                    #             total_time_worked += worktime.end_time - worktime.start_time

                    #     # Переводим общее время в формат часов и минут
                    #     total_hours_worked = total_time_worked.seconds // 3600
                    #     total_minutes_worked = (total_time_worked.seconds % 3600) // 60

                    #     return render(request, 'monthly_report.html', {'worktimes': worktimes, 'total_hours_worked': total_hours_worked, 'total_minutes_worked': total_minutes_worked})
    



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

