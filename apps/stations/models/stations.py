# coding: utf8
from django.db import models
from django.db.models.signals import post_delete, pre_save
from .locations import LocationModel
from apps.utils import create_id

"""
Add Model to record the historical events 
"""
EVENT_TYPE = [
    ("Delete", "delete"),
    ("Create", "create"),
]


class Historical(models.Model):
    """ Historical object is the representation of historical events with objects

                       Fields:
                           event -- Type of event(CRUD).
                           model_type -- Model where event happen.
                           created_at -- Date of creation
                           updated_at -- Date of last modification
                   """
    event = models.CharField(max_length=100, choices=EVENT_TYPE, default="Delete")
    model_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}-{}".format(self.event, self.model_type)


class StationModel(models.Model):
    """ Station object is the representation of physical station

                   Fields:
                       id -- This is the unique identifier for object instance.
                       location -- Location of the station(coordinates).
                       order -- Order of the station.
                       is_active -- If the route is active.
                       created_at -- Date of creation
                       updated_at -- Date of last modification
               """
    id = models.CharField(
        default=create_id("sta_"), primary_key=True, max_length=30, unique=True
    )
    location = models.ForeignKey(LocationModel, on_delete=models.DO_NOTHING)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]


"""
Add Signal for post_delete of Station Model and save the event in Historial 
"""


def pre_create_id(sender, instance, **kwargs):
    instance.id = create_id("sta_")


def remove_location(sender, instance, **kwargs):
    name_class = sender._meta.object_name
    Historical.objects.create(event="Delete", model_type=name_class)


post_delete.connect(remove_location, sender=StationModel)
pre_save.connect(pre_create_id, sender=StationModel)
