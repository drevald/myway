from django.db import models
from datetime import datetime

class ShowObject(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length = 32)

class ShowPoint(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=32, null=True, default="Point")

class Photo(models.Model):
    thumbnail = models.BinaryField()
    md5 = models.CharField(max_length = 32)
    local = models.CharField(max_length = 32)
    remote = models.CharField(max_length = 32)

class ShowPointObject(models.Model):
    object = models.ForeignKey(ShowObject, on_delete = models.CASCADE)
    point = models.ForeignKey(ShowPoint, on_delete = models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete = models.CASCADE)

class Tag(models.Model):
    name = models.CharField(max_length = 32)

class Person(models.Model):
    first_name = models.CharField(max_length = 32)
    last_name = models.CharField(max_length = 32)
    middle_name = models.CharField(max_length = 32)
    birth_date = models.DateField()
    death_date = models.DateField()
    biography = models.TextField()

class Event(models.Model):
    name = models.CharField(max_length = 32)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

class PersonTag(models.Model):
    person = models.ForeignKey(Person, on_delete = models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete = models.CASCADE)

class EventTag(models.Model):
    person = models.ForeignKey(Person, on_delete = models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete = models.CASCADE)

class Trip(models.Model):
    name = models.CharField(max_length = 32)

class TripPoint(models.Model):
    trip = models.ForeignKey(Trip, on_delete = models.CASCADE)
    point = models.ForeignKey(ShowPoint, on_delete = models.CASCADE)
    order = models.IntegerField()
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['trip', 'point'], name="trip_point")
        ]

class TripTag(models.Model):
    trip = models.ForeignKey(Trip, on_delete = models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete = models.CASCADE)

