from wsgiref.validate import validator

from django.core.validators import MinLengthValidator
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

# class User(models.Model):
#     name = models.CharField(max_length=20, validators=[MinLengthValidator(3)]),
#     last_name = models.CharField(max_length=20, validators=[MinLengthValidator(3)]),
