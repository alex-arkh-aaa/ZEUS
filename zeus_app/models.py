from wsgiref.validate import validator

from django.core.validators import MinLengthValidator
from django.db import models
from django.core.exceptions import ValidationError
from users.models import User
# Create your models here.


class Booking(models.Model):
    '''Класс для бронирования корта. Связан с юзером, связан с CourtTimePrice по id и подгружет цену'''
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    court_id = models.IntegerField(choices=[(1, 'Желтый корт № 1'), (2, 'Синий корт № 2'), (3, 'Оранжевый корт № 3')])
    bookind_datetime = models.DateTimeField()
    status = models.CharField()
    price = models.IntegerField()

    def __str__(self):
        return f'User_id - {self.user_id}, время - {self.bookind_datetime}, court_id - {self.court_id}, статус - {self.status}'


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
    week_day = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')])
    time = models.TimeField()
    price = models.IntegerField()

    def __str__(self):
        return f'{self.week_day} день недели, {self.time} - {self.price}'
    


class Trainings(models.Model):
    '''Класс предназначен для админов(тренеров). При планировании класса админ создает новую запись, после чего в таблице 
    AllTrainingSlots создается 8 новых записей, которые можно будет занять юзерам на странице сайта 'Тренировки' '''
    trainer_name = models.CharField(choices=[('Александр Игнатов', 'Саша'), ('Анастасия Бунарева', 'Настя')])
    start_datetime = models.DateTimeField()
    
    def __str__(self):
        return f'{self.start_datetime}, тренер - {self.trainer_name}'
    

class AllTrainingSlots(models.Model):
    '''Класс связан с Trainings. При добавлении тренировки, здесь создаются 8 строк - мест, которые могту занять юзеры на тренировку.'''
    training_id = models.IntegerField()
    slot_number = models.IntegerField()
    user_id = models.IntegerField()
    status = models.IntegerField()

    def __str__(self):
        return f'Номер тренировки: {self.training_id}, Место: {self.slot_number}, user_id: {self.user_id}'
    