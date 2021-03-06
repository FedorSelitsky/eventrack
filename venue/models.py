from django.contrib.gis.db import models


class Location(models.Model):
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255, default='')
    country = models.CharField(max_length=255)

    coordinates = models.PointField(null=True)

    def __str__(self):
        return '{}, {}'.format(self.city, self.country)


class Venue(models.Model):
    zip = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=255, default='')
    street = models.CharField(max_length=255, default='')

    capacity = models.IntegerField(null=True)
    description = models.TextField(default='')

    coordinates = models.PointField(null=True)

    website = models.URLField(default='')
    songkick_url = models.URLField(default='')

    location = models.ForeignKey(
        Location,
        null=True,
        related_name='venues',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return '{} @ {}'.format(self.name, self.location)
