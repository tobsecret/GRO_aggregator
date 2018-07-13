from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=140)
    body = models.TextField()
    date = models.DateTimeField()
    address = models.CharField(max_length=140)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.title
