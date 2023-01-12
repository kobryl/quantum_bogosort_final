from django.db import models

# Create your models here.
class Tf(models.Model):
    tf = models.CharField(max_length=200)

    def __str__(self):
        return self.tf