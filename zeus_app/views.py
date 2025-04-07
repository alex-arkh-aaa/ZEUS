from django.shortcuts import render


# Create your views here.
def show_main_page(request):
    print('Была открыта главная страница')
    print(request)
    return render(request, 'main_page.html')


def show_trainings(request):
    return render(request, 'trainings.html')


def show_bookings(request):
    return render(request, 'bookings.html')


def show_booking_rules(request):
    return render(request, 'booking_rules.html')

def post_comment(request):
    print('post comment')
    ...
