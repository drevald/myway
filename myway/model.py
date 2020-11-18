from django.db import models
from datetime import datetime

class ShowObject(models.Model):
    name = models.CharField()

class ShowPoint(models.Model):
    latitude = models.IngegerField()
    longitude = models.IngegerField()

class ShowPointObject(models.Model):
    object = models.ForeignKey(ShowObject, on_delete = models.CASCADE)
    point = models.ForeignKey(ShowPoint, on_delete = models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete = models.NONE)

class Tag(models.Model):
    name = models.CharField()

class Photo(models.Model):
    thumbnail = models.BlobField()
    md5 = models.CharField()
    local = models.CharField()
    remote = models.CharField()

class Person(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    middle_name = models.CharField()
    birth_date = models.DateField()
    death_date = models.DateField()
    biography = models.CharField()

class Event(models.Model):
    name = models.CharField()
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.CharField()

class PersonTag(models.Model):
    person = models.ForeignKey(Person, on_delete = models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete = models.CASCADE)

class EventTag(models.Model):
    person = models.ForeignKey(Person, on_delete = models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete = models.CASCADE)

class Trip(models.Model):
    name = models.CharField()

class TripPoint(models.Model):
    trip = model.ForeignKey(Trip, on_delete = CASCADE)
    point = model.ForeignKey(ShowPoint, on_delete = CASCADE)
    order = model.IngegerField

class TripTag(models.Model):
    trip = models.ForeignKey(Trip, on_delete = CASCADE)
    tag = models.ForeignKey(Tag, on_delete = CASCADE)