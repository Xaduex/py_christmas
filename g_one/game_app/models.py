from django.db import models

# Create your models here.

class Place(models.Model):
    description = models.TextField(blank=True)
    short_description = models.TextField(max_length=200)

    def __str__(self):
        return self.short_description
