"""
Models for the system that control the database
"""
from django.db import models

class Song(models.Model):
    """
    Model for songs in the database
    """
    title = models.CharField(max_length=200)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Meme(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name