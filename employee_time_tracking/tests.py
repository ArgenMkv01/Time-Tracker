from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import WorkTime, Employee, Task

class DailyReportTests(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(name='Test Employee')
        self.task1 = Task.objects.create(name='Test Task 1')
        self.task2 = Task.objects.create(name='Test Task 2')
        self.worktime1 = WorkTime.objects.create(
            employee=self.employee,
            task=self.task1,
            start_time=timezone.now() - timezone.timedelta(hours=2),
            end_time=timezone.now() - timezone.timedelta(hours=1)
        )
        self.worktime2 = WorkTime.objects.create(
            employee=self.employee,
            task=self.task2,
            start_time=timezone.now() - timezone.timedelta(hours=1),
            end_time=timezone.now()
        )

    def test_daily_report_view(self):
        response = self.client.get(reverse('daily_report'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Total hours worked today')
        self.assertContains(response, 'hours')

class WeeklyReportTests(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(name='Test Employee')
        self.task1 = Task.objects.create(name='Test Task 1')
        self.task2 = Task.objects.create(name='Test Task 2')
        self.worktime1 = WorkTime.objects.create(
            employee=self.employee,
            task=self.task1,
            start_time=timezone.now() - timezone.timedelta(days=2, hours=2),
            end_time=timezone.now() - timezone.timedelta(days=2, hours=1)
        )
        self.worktime2 = WorkTime.objects.create(
            employee=self.employee,
            task=self.task2,
            start_time=timezone.now() - timezone.timedelta(days=1, hours=1),
            end_time=timezone.now() - timezone.timedelta(days=1)
        )

    def test_weekly_report_view(self):
        response = self.client.get(reverse('weekly_report'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Total hours worked this week')
        self.assertContains(response, 'hours')
