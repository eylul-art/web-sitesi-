from django.db import models

class Language(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10) # örn: en, tr

    def __str__(self):
        return self.name

class Level(models.Model):
    code = models.CharField(max_length=10) # örn: A1, B2

    def __str__(self):
        return self.code
# Create your models here.
