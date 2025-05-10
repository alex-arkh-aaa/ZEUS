from django.contrib import admin
from .models import Booking, Comment, CourtTimePrice, Trainings, AllTrainingSlots
# Register your models here.

admin.site.register(Trainings)

admin.site.register(AllTrainingSlots)

admin.site.register(CourtTimePrice)

admin.site.register(Comment)

admin.site.register(Booking)
