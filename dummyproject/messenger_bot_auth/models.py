from django.db import models

# Create your models here.

#
# class Profile(models.Model):
#     class Meta:
#         db_table = 'profile'
#
#     messenger_app_user_id = models.CharField(null=False, unique=True, max_length=255)


class CrowdtanglePreference(models.Model):

    class Meta:
        db_table = 'crowdtangle_preferences'

    # user_pref_id = models.AutoField(primary_key=True)
    search_preference = models.CharField(max_length=255)
    user_bot_id = models.IntegerField()
