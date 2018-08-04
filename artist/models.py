from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField(blank=True)
    thumb_url = models.URLField(blank=True)

    events = models.ManyToManyField(
        'event.Event',
        related_name='artists',
        blank=True,
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
