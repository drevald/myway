from django.db import models
from datetime import datetime

class Photo(models.Model):
    thumbnail = models.TextField(null=False)
    md5 = models.CharField(max_length = 32, null = False)
    local = models.CharField(max_length = 32)
    remote = models.CharField(max_length = 32)

class Tag(models.Model):
    name = models.CharField(max_length = 32)

class Event(models.Model):
    name = models.CharField(max_length = 32)
    start_date = models.DateField(null = True, blank=True)
    end_date = models.DateField(null = True, blank=True)
    description = models.TextField(null = True, blank=True)    
    tags = models.ManyToManyField(Tag, blank=True)

class Person(models.Model):
    first_name = models.CharField(max_length = 32)
    last_name = models.CharField(max_length = 32, null = True, blank=True)
    middle_name = models.CharField(max_length = 32, null = True, blank=True)
    birth_date = models.DateField()
    death_date = models.DateField(null = True, blank=True)
    biography = models.TextField(null = True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    events = models.ManyToManyField(Event, blank=True)

class ShowObject(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length = 128, null = True, blank=True)
    name = models.CharField(max_length = 32)
    photo = models.ForeignKey(Photo, on_delete = models.CASCADE, null = True)
    persons = models.ManyToManyField(Person, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    events = models.ManyToManyField(Event, blank=True)


class ShowPoint(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=32, null=True, default="Point")

class ShowPointObject(models.Model):
    object = models.ForeignKey(ShowObject, on_delete = models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete = models.CASCADE)

class PersonTag(models.Model):
    person = models.ForeignKey(Person, on_delete = models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete = models.CASCADE)

class EventTag(models.Model):
    person = models.ForeignKey(Person, on_delete = models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete = models.CASCADE)

class Trip(models.Model):
    name = models.CharField(max_length = 32)

class TripPoint(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=32, null=True, default="Point")    
    trip = models.ForeignKey(Trip, related_name="points", on_delete = models.CASCADE)
    order = models.IntegerField()

class TripPointObject(models.Model):
    trip_point = models.ForeignKey(TripPoint, related_name="show_objects", on_delete = models.CASCADE)
    object = models.ForeignKey(ShowObject, on_delete=models.CASCADE)
    story = models.TextField(null = True, blank= True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['trip_point', 'object'], name="trip_point_object")
        ]

class TripTag(models.Model):
    trip = models.ForeignKey(Trip, on_delete = models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete = models.CASCADE)
