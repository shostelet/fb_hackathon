from django.db import models

# Create your models here.


class Profile(models.Model):

    messenger_app_user_id = models.IntegerField()


class Topic(models.Model):

    name = models.CharField(max_length=255)
    profile = models.ForeignKey(Profile, related_name="topics")
