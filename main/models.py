from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=CASCADE)
    link = models.URLField()
    description = models.TextField(max_length=6000)
    release_date = models.DateField()
    averageRating = models.FloatField(default=0)
    image = models.URLField(default=None, null=True)

    def __unicode__(self):
        return self.name


    def __str__(self):
        return self.name