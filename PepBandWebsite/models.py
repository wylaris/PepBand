from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=200)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.title