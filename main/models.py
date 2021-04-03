from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.URLField()
    description = models.TextField(max_length=6000)
    publish_date = models.DateField()
    averageRating = models.FloatField(default=0)
    image = models.URLField(default=None, null=True)

    def __unicode__(self):
        return self.title


    def __str__(self):
        return self.title


class Review(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    design_rating = models.FloatField(default=0)
    usability_rating = models.FloatField(default=0)
    content_rating = models.FloatField(default=0)

    def __str__(self):
        return self.user.username
