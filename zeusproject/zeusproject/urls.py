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

from django.contrib import admin
from django.urls import path, include
from zeus_app.views import show_main_page, show_trainings, show_bookings, show_booking_rules

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', show_main_page),
    path('bookings/', show_bookings),
    path('trainings/', show_trainings),
    path('booking_rules', show_booking_rules),
    path('accounts/', include('django.contrib.auth.urls')),

]
