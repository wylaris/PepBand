"""
Models for the system that control the database
"""
from django.db import models


class Song(models.Model):
    """
    Model for songs in the database
    """
    CHOICES = (
        ('Pu', 'Public'),
        ('Pr', 'Private'),
    )
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=2, choices=CHOICES, default='Pr')

    def __str__(self):
        return self.title


class eBoard(models.Model):
    """
    Model for eBoard members
    """
    CHOICES = (
        ('T', 'Treasurer'),
        ('C', 'Conductor'),
        ('VP', 'Vice President'),
        ('S', 'Secretary'),
        ('P', 'President'),
    )
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    position = models.CharField(max_length=2, choices=CHOICES)
    cell = models.CharField(max_length=14)
    email = models.CharField(max_length=15)

    def __str__(self):
        return self.firstName + self.lastName


class Section(models.Model):
    """
    Model for eBoard members
    """
    CHOICES = (
        ('F', 'Flutes'),
        ('Cl', 'Clarinets'),
        ('AS', 'Alto Saxophones'),
        ('Tpt', 'Trumpets'),
        ('M', 'Mellophones'),
        ('TS', 'Tenor Saxophones'),
        ('Trb', 'Trombones'),
        ('Tub', 'Tubas'),
        ('P', 'Percussion'),
    )
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    section = models.CharField(max_length=2, choices=CHOICES)
    cell = models.CharField(max_length=14)
    email = models.CharField(max_length=15)

    def __str__(self):
        return self.firstName + self.lastName
