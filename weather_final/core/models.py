from django.db import models
from datetime import datetime
# Create your models here.
class City (models.Model):
    name= models.CharField(max_length=64)
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return(f"{self.name} :: {self.time}")