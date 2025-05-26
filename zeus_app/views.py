import datetime
from django.shortcuts import render
from .models import Comment, Booking, Trainings, AllTrainingSlots, CourtTimePrice
from django.db.models import Q
from django.contrib import messages

# Create your views here.
def show_main_page(request):
    if request.method == 'POST':
        post_comment(request)

    coms = Comment.objects.all()
    data = {'comments': coms}
    return render(request, 'main_page.html', context = data)


def show_trainings(request):
    return render(request, 'trainings.html')


def show_bookings(request):
    return render(request, 'bookings.html')


def show_booking_rules(request):
    return render(request, 'booking_rules.html')

def trainings_light(request):
    if request.method == 'POST':
        training_id = request.POST.get('training_id')
        user_id = request.user.id
        
        try:
            training = Trainings.objects.get(id=training_id)
            
            # Проверяем количество записей
            booked_slots = AllTrainingSlots.objects.filter(
                training_id=training_id,
                status=1  # 1 = "забронировано"
            ).count()
            
            if booked_slots >= 8:
                messages.warning(request, 'Извините! Места кончились!')
            elif AllTrainingSlots.objects.filter(training_id=training_id, user_id=user_id).exists():
                messages.warning(request, 'Вы уже записаны на эту тренировку')
            else:
                AllTrainingSlots.objects.create(
                    training_id=training_id,
                    user_id=user_id,
                    status=1,
                    slot_number=1
                )
                messages.success(request, 'Вы успешно записаны на тренировку!')
                
        except Trainings.DoesNotExist:
            messages.error(request, 'Тренировка не найдена')

    trainings = get_upcoming_trainings_with_slots('light')

    data = {'trainings': trainings}
    return render(request, 'trainings_light.html', context=data)

def trainings_medium(request):
    if request.method == 'POST':
        training_id = request.POST.get('training_id')
        user_id = request.user.id
        
        try:
            training = Trainings.objects.get(id=training_id)
            
            # Проверяем количество записей
            booked_slots = AllTrainingSlots.objects.filter(
                training_id=training_id,
                status=1  # 1 = "забронировано"
            ).count()
            
            if booked_slots >= 8:
                messages.warning(request, 'Извините! Места кончились!')
            elif AllTrainingSlots.objects.filter(training_id=training_id, user_id=user_id).exists():
                messages.warning(request, 'Вы уже записаны на эту тренировку')
            else:
                AllTrainingSlots.objects.create(
                    training_id=training_id,
                    user_id=user_id,
                    status=1,
                    slot_number=1
                )
                messages.success(request, 'Вы успешно записаны на тренировку!')
                
        except Trainings.DoesNotExist:
            messages.error(request, 'Тренировка не найдена')

    trainings = get_upcoming_trainings_with_slots('medium')

    data = {'trainings': trainings}
    return render(request, 'trainings_medium.html', context=data)


def trainings_hard(request):
    if request.method == 'POST':
        training_id = request.POST.get('training_id')
        user_id = request.user.id
        
        try:
            training = Trainings.objects.get(id=training_id)
            
            # Проверяем количество записей
            booked_slots = AllTrainingSlots.objects.filter(
                training_id=training_id,
                status=1  # 1 = "забронировано"
            ).count()
            
            if booked_slots >= 8:
                messages.warning(request, 'Извините! Места кончились!')
            elif AllTrainingSlots.objects.filter(training_id=training_id, user_id=user_id).exists():
                messages.warning(request, 'Вы уже записаны на эту тренировку')
            else:
                AllTrainingSlots.objects.create(
                    training_id=training_id,
                    user_id=user_id,
                    status=1,
                    slot_number=1
                )
                messages.success(request, 'Вы успешно записаны на тренировку!')
                
        except Trainings.DoesNotExist:
            messages.error(request, 'Тренировка не найдена')

    trainings = get_upcoming_trainings_with_slots('hard')

    data = {'trainings': trainings}
    return render(request, 'trainings_hard.html', context=data)

def post_comment(request):

    print('post comment')
    comment_text = request.POST.get('comment')
    rating_value = request.POST.get('rating_value')

    if not comment_text or not rating_value:
        return render(request, 'main_page.html')
    
    try:
        rating = int(rating_value)
        if not 1 <= rating <= 5:
            return render(request, 'main_page.html')
        
    except ValueError:
        return render(request, 'main_page.html')

    # Создаем и сохраняем комментарий
    comment = Comment(user_id = request.user, text = comment_text, rating_value = rating)
    comment.save()


def get_upcoming_trainings_with_slots(level):
    # Получаем текущую дату и время
    now = datetime.datetime.now()    
    # 1. Получаем все будущие тренировки
    upcoming_trainings = Trainings.objects.filter(
        Q(date__gt=now.date()) | 
        Q(date=now.date(), time__gt=now.time())
    ).filter(level=level).order_by('date', 'time')
    
    # 2. Для каждой тренировки добавляем количество свободных мест
    for training in upcoming_trainings:
        # Считаем занятые слоты (где user_id не пустой)
        booked_slots = AllTrainingSlots.objects.filter(
            training_id=training.id,
            user_id__isnull=False
        ).count()
        
        # Предполагаем, что всего 8 слотов на тренировку
        training.free_slots = 8 - booked_slots
        print(booked_slots)
    
    return upcoming_trainings