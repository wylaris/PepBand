"""
Models for the system that control the database
"""
from django.db import models


class Song(models.Model):
    """
    Model for songs in the database
    """
    CHOICES = (
        ('Public', 'Public'),
        ('Private', 'Private'),
    )
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=7, choices=CHOICES, default='Private')
    slug = models.CharField(max_length=200, blank=False)
    video = models.CharField(max_length=100, default="", blank=True)
    notes = models.CharField(max_length=500, default="None")

    def __str__(self):
        return self.title


class eBoard(models.Model):
    """
    Model for eBoard members
    """
    CHOICES = (
        ('Treasurer', 'Treasurer'),
        ('Conductor', 'Conductor'),
        ('Vice President', 'Vice President'),
        ('Secretary', 'Secretary'),
        ('President', 'President'),
    )
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    position = models.CharField(max_length=15, choices=CHOICES)
    cell = models.CharField(max_length=10)
    email = models.CharField(max_length=15)
    slug = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.firstName +" " + self.lastName


class Section(models.Model):
    """
    Model for eBoard members
    """
    CHOICES = (
        ('Flutes', 'Flutes'),
        ('Clarinets', 'Clarinets'),
        ('Saxophones', 'Alto Saxophones'),
        ('Trumpets', 'Trumpets'),
        ('Mellophones', 'Mellophones'),
        ('Tenor Saxophones', 'Tenor Saxophones'),
        ('Trombones', 'Trombones'),
        ('Tubas', 'Tubas'),
        ('Percussion', 'Percussion'),
    )
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    section = models.CharField(max_length=16, choices=CHOICES)
    cell = models.CharField(max_length=10)
    email = models.CharField(max_length=15)

    def __str__(self):
        return self.firstName +" " + self.lastName
