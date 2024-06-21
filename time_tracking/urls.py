from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login/', permanent=True)),  # Перенаправление на страницу входа
    path('', include('employee_time_tracking.urls')),  # Подключение URL приложения
]