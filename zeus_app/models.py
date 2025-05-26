from wsgiref.validate import validator

from django.core.validators import MinLengthValidator
from django.db import models
from django.core.exceptions import ValidationError
from users.models import User
from datetime import date

# Create your models here.


class Booking(models.Model):
    '''Класс для бронирования корта. Связан с юзером, связан с CourtTimePrice по id и подгружет цену'''
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    court_id = models.IntegerField(choices=[(1, 'Желтый корт № 1'), (2, 'Синий корт № 2'), (3, 'Оранжевый корт № 3')])
    booking_datetime = models.DateTimeField()
    status = models.CharField()
    price = models.IntegerField()

    def __str__(self):
        return f'User_id - {self.user_id}, время - {self.booking_datetime}, court_id - {self.court_id}, статус - {self.status}'


class Comment(models.Model):
    '''Класс комментария. Связан только с юзером'''
    user_id = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=-1)
    rating_value = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    text = models.TextField(help_text='Напишите свой комментарий, пожалуйста!', )
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'User_id - {self.user_id}, оценка - {self.rating_value}, дата - {self.created_at}'


class CourtTimePrice(models.Model):
    '''Класс для админа. Выставляет цену на корт в каждое время каждого дня.
    Далее данные подгружаются и используется цена для бронирования'''
    WEEKDAY_CHOICES = [
        ('Понедельник', 'Понедельник'),
        ('Вторник', 'Вторник'),
        ('Среда', 'Среда'),
        ('Четверг', 'Четверг'),
        ('Пятница', 'Пятница'),
        ('Суббота', 'Суббота'),
        ('Воскресенье', 'Воскресенье'),
    ]
    time_choices = [('06:00', '06:00'), ('08:00', '08:00'), ('10:00', '10:00'), ('12:00', '12:00'), ('14:00', '14:00'), 
                    ('16:00', '16:00'), ('18:00', '18:00'), ('20:00', '20:00'), ('22:00', '22:00')]

    week_day = models.CharField(choices=WEEKDAY_CHOICES)
    time = models.CharField(choices=time_choices, default='00:00')
    price = models.IntegerField()

    def __str__(self):
        formatted_time = self.time.zfill(5)  # Add leading zero if needed

        print(self.time)
        return f'{self.week_day}, {formatted_time} - {self.price} руб.'
    


class Trainings(models.Model):
    '''Класс предназначен для админов(тренеров). При планировании класса админ создает новую запись, после чего в таблице 
    AllTrainingSlots создается 8 новых записей, которые можно будет занять юзерам на странице сайта 'Тренировки' '''
    time_choices = [('10:00', '10:00'), ('11:00', '11:00'), ('12:00', '12:00'), ('13:00', '13:00'),
                    ('14:00', '14:00'), ('15:00', '15:00'), ('16:00', '16:00'), ('17:00', '17:00'),
                    ('18:00', '18:00'), ('19:00', '19:00'), ('20:00', '20:00'), ('21:00', '21:00')]
    

    trainer_name = models.CharField(choices=[('Александр Игнатов', 'Саша'), ('Анастасия Бунарева', 'Настя')])
    level = models.CharField(choices=[('light', 'Начальный'), ('medium', 'Уверенный'), ('hard', 'Продвинутый')], default='light')
    date = models.DateField(default=date.today)
    time = models.CharField(choices=time_choices, default='00:00') 
    
    def __str__(self):
        # date_str = self.date.strftime('%Y-%m-%d')  # Форматируем дату
        # time_str = self.time.strftime('%H:%M')     # Форматируем время
        return f'Время: {self.time}, Дата: {self.date}, Тренер: {self.trainer_name}, уровень: {self.level}'
    

class AllTrainingSlots(models.Model):
    '''Класс связан с Trainings. При добавлении тренировки, здесь создаются 8 строк - мест, которые могту занять юзеры на тренировку.'''
    training_id = models.IntegerField()
    slot_number = models.IntegerField()
    user_id = models.IntegerField()
    status = models.IntegerField()

    def __str__(self):
        return f'Номер тренировки: {self.training_id}, Место: {self.slot_number}, user_id: {self.user_id}'
    