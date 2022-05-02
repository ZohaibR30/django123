from django.db import models

# Create your models here.
class websearching(models.Model):
    link = models.CharField(max_length=120)
    title = models.TextField()
    score = models.TextField()
    angle = models.TextField()

# def __str__(self):
#         return self.link