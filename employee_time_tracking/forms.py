from django import forms
from .models import WorkTime, Attendance, Project, Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Employee



class WorkTimeForm(forms.ModelForm):
    class Meta:
        model = WorkTime
        fields = ['user', 'start_time', 'end_time', 'task', 'pause_time'] 
        
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date']

class EmployeeRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email', max_length=100, required=True)
    name = forms.CharField(label='Name', max_length=100, required=True)
    position = forms.CharField(label='Position', max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'check_in_time', 'check_out_time', 'date']

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'name', 'description', 'start_date', 'end_date', 'completed']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }