# coding: utf8
from django.db import models
from apps.utils import create_id
from django.db.models.signals import pre_save

# from django.contrib.gis.db import models


class LocationModel(models.Model):
    """ Location object is the representation of physical station

        Fields:
            id -- This is the unique identifier for object instance.
            name -- This is the common identifier for a physical location.
            coordinates --  Latitude and Longuitude as string.
                            example. "19.4094937,-99.1634261"
            geometry -- Similar to coordinate but using with postgis
    """

    id = models.CharField(
        default=create_id("loc_"), primary_key=True, max_length=30, unique=True
    )
    name = models.CharField(max_length=100)
    # latitude = models.DecimalField(max_digits=19, decimal_places=16)
    # longitude = models.DecimalField(max_digits=19, decimal_places=16)
    coordinates = models.CharField(max_length=100, default="")
    # geometry = models.PointField()  #TODO:Install GDAL Library

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]


def pre_create_id(sender, instance, **kwargs):
    instance.id = create_id("loc_")


pre_save.connect(pre_create_id, sender=LocationModel)
