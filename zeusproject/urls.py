"""
URL configuration for zeusproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from xml.etree.ElementInclude import include
#django_auth/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # Импортируем настройки проекта
from django.conf.urls.static import static  # Импортируем функцию static для работы со статическими файлами

from zeus_app.views import show_main_page, show_trainings, show_bookings, show_booking_rules, trainings_light, trainings_medium, trainings_hard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', show_main_page, name='main_page'),

    # Pay attention to the order: more specific URL should go before less specific URL
    path('bookings/<int:week_offset>/', show_bookings, name='booking_table_with_offset'),
    path('bookings/', show_bookings, name='bookings'),


    path('trainings/', show_trainings),
    path('trainings/light/', trainings_light, name='trainings_light'),
    path('trainings/medium/', trainings_medium, name='trainings_medium'),
    path('trainings/hard/', trainings_hard, name='trainings_hard'),
    path('booking_rules/', show_booking_rules),
    path('user/', include('users.urls', namespace='users')),
]

if settings.DEBUG:  # Если включен режим отладки (DEBUG=True)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Добавляем URL-адреса для медиа-файлов

# Serve static files during development (alternative way)
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
