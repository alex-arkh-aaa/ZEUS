from xml.etree.ElementInclude import include
#django_auth/urls.py

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings  # Импортируем настройки проекта
from django.conf.urls.static import static  
from rest_framework import permissions  # <-- Убедитесь, что этот импорт есть
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from zeus_app.views import show_main_page, show_trainings, show_bookings, show_booking_rules, trainings_light, trainings_medium, trainings_hard

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",  # Название вашего API
        default_version='v1', # Версия API
        description="Описание вашего API", # Описание
        terms_of_service="https://www.google.com/policies/terms/", # Условия использования (необязательно)
        contact=openapi.Contact(email="your_email@example.com"), # Контакты (необязательно)
        license=openapi.License(name="BSD License"), # Лицензия (необязательно)
    ),
    public=True,
    permission_classes=[permissions.AllowAny],  # Или ваши классы разрешений
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', show_main_page, name='main_page'),
    re_path(r'bookings/(?P<week_offset>-?\d+)/', show_bookings, name='bookings_with_offset'),
    #path('bookings/', show_bookings, name='bookings'),
    path('trainings/', show_trainings),
    path('trainings/light/', trainings_light, name='trainings_light'),
    path('trainings/medium/', trainings_medium, name='trainings_medium'),
    path('trainings/hard/', trainings_hard, name='trainings_hard'),
    path('booking_rules/', show_booking_rules, name='booking_rules'),
    path('user/', include('users.urls', namespace='users')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:  # Если включен режим отладки (DEBUG=True)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Добавляем URL-адреса для медиа-файлов

# Serve static files during development (alternative way)
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
