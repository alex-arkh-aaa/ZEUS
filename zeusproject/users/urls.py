from django.urls import path
from . import views  # Импортируем views из текущего приложения (users)

app_name = 'users'  # Важно для пространств имен URL

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logoutUser, name='logout'),  # Если есть представление logout
    path('home/', views.home, name='home'),        # Если есть представление home
]