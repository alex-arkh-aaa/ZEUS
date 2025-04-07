from wsgiref.validate import validator

from django.core.validators import MinLengthValidator
from django.db import models
from django.core.exceptions import ValidationError
from users.models import User
# Create your models here.


class Booking(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    court_number = models.IntegerField(choices=[(1, 'Желтый корт № 1'), (2, 'Синий корт № 2'), (3, 'Оранжевый корт № 3')])
    bookind_datetime = models.DateTimeField()





class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=-1)
    rating_value = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    text = models.TextField(help_text='Напишите свой комментарий, пожалуйста!', )