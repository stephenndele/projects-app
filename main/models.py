from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save 
from django.dispatch import receiver 

# from tinymce.models import HTMLField

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=250)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name= 'projects')
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


class Profile(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.CharField(max_length=1000, blank=True, null=True)
    image = models.ImageField(
            null=True, 
            blank=True, 
            height_field='height_field', 
            width_field='width_field'
    )
    # projects = models.ManyToManyField(Project)

    @receiver(post_save, sender=User) #add this
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User) #add this
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()