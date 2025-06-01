from datetime import datetime, timedelta, date
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


def show_bookings(request, week_offset=0):
    if request.method == 'POST':
        court_id = request.POST.get('court_id')
        booking_datetime_str = request.POST.get('booking_datetime')
        price = request.POST.get('price')
        booking_datetime = None
        try:
            booking_datetime = datetime.strptime(booking_datetime_str, '%Y-%m-%d %H:%M')            
            price = float(price)
        except (ValueError, TypeError) as e:
            messages.error(request, "Неверный формат даты, времени или цены.")
        if booking_datetime is None:
            messages.error(request, "Не удалось обработать дату и время бронирования.")
        user_id = request.user
        try:
            booking = Booking(
                user_id=user_id,
                court_id=court_id,
                booking_datetime=booking_datetime,
                status='Подтверждено',
                price=price
            )
            booking.save()
            messages.success(request, "Корт успешно забронирован!")
            
        except Exception as e:
            print(f"Error during saving: {e}")
            messages.error(request, f"Произошла ошибка при сохранении бронирования: {e}")
            #return redirect('your_booking_table_url')


    data = booking_table(request, week_offset)

    return render(request, 'bookings.html', context=data)


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



def booking_table(request, week_offset=0):
    """Отображает таблицу бронирований на неделю со смещением."""
    week_offset = int(week_offset)
    print(week_offset)
    # 1. Определяем текущую неделю со смещением
    today = date.today()
    start_date = today + timedelta(days=-today.weekday(), weeks=week_offset)
    end_date = start_date + timedelta(days=6)
    days = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    print(days)


    # 2. Получаем временные слоты из базы данных (CourtTimePrice)
    time_slots_data = CourtTimePrice.objects.values('time').distinct().order_by('time')
    time_slots = [datetime.strptime(t['time'], '%H:%M').time() for t in time_slots_data]
    time_slot_strings = [ts.strftime('%H:%M') for ts in time_slots]

    # 3. Получаем варианты выбора корта из модели Booking
    COURT_CHOICES = Booking._meta.get_field('court_id').choices

    # Создаем словарь для соответствия чисел дням недели
    weekday_mapping = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота',
        6: 'Воскресенье',
    }

    # 4. Создаем структуру данных для таблицы
    table_data = []
    for day in days:
        date_obj = datetime.strptime(day, '%Y-%m-%d').date()
        for time_slot in time_slots:
            time_str = time_slot.strftime('%H:%M')
            for court_choice in COURT_CHOICES:
                court_id = court_choice[0]
                # Prepare the composite key:
                key = f"{day}_{time_str}_{court_id}"
                table_data.append({
                    'key': key,
                    'day': day,
                    'time_slot': time_str,
                    'court_id': court_id,
                    'court_name': court_choice[1],
                    'available': True,
                    'booked_count': 0,
                    'price': "Цена не установлена",  # Set default price
                })

    # 5. Заполняем структуру данными о бронированиях и ценах
    for item in table_data:
        date_obj = datetime.strptime(item['day'], '%Y-%m-%d').date()
        weekday_num = date_obj.weekday()  # Get the weekday number (0-6) for each item
        weekday = weekday_mapping[weekday_num]  # Get the day name from the mapping for each item
        try:
            court_time_price = CourtTimePrice.objects.get(week_day=weekday, time=item['time_slot'])
            item['price'] = court_time_price.price
        except CourtTimePrice.DoesNotExist:
            item['price'] = "Цена не установлена"  # or some default value

        # Count bookings for each court
        bookings_count = Booking.objects.filter(
            court_id=item['court_id'],
            booking_datetime__date=date_obj,
            booking_datetime__time=datetime.strptime(item['time_slot'], '%H:%M').time()
        ).count()
        item['booked_count'] = bookings_count

        # Mark as unavailable if court is booked
        if bookings_count >= 1:
            item['available'] = False
        

    # 6. Передаем данные
    data = {
        'days': days,
        'time_slots': time_slot_strings,
        'table_data': table_data,
        'courts': COURT_CHOICES,
        'week_offset': week_offset,  # Add week_offset to the context
    }
    return data




















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
    now = datetime.now()    
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
    
    return upcoming_trainings





