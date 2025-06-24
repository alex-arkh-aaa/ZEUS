# Import necessary modules and models
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
logger = logging.getLogger(__name__)  # Get the logger for the current module


@login_required
def home(request):
    return render(request, 'zeus_app/main_page.html')


def login_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user with the provided username and password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log in the user and redirect to the home page upon successful login
            login(request, user)
            logger.info(f"Пользователь {username} успешно вошел в свой аккаунт.")

            return redirect('http://127.0.0.1:8000/')
        else:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Ваш ник или пароль введен неверно!") # Общее сообщение об ошибке
            return redirect('http://127.0.0.1:8000/user/login/')

    # Render the login page template (GET request)
    return render(request, 'users/login.html')



def register_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username exists before creating user
        if User.objects.filter(username=username).exists():  # Упрощаем проверку
            # Display an information message if the username is taken
            messages.info(request, "Извините, этот никнейм уже занят")
            return redirect('/user/register/')

        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email
        )

        user.set_password(password)
        user.save()
        logger.info(f"Пользователь {username} успешно создал свой аакаунт.")

        messages.success(request, "Аккаунт успешно создан!.")  # Меняем сообщение
        return redirect('/user/login/')  # Перенаправляем на страницу входа

    # Render the registration page template (GET request)
    return render(request, 'users/register.html')


def logoutUser(request):
    logger.info(f"Пользователь {request.user.username} вышел из своего аккаунта.")

    logout(request) # Выходим из системы

    return redirect('/')  # Redirect to the main page after logout

