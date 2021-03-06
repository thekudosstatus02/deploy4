from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models
from embed_video.fields import EmbedVideoField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

class SiteDesc(models.Model):
    site_desc = models.CharField(max_length=200, default='SOME STRING')


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(blank=False, upload_to='user_images')
    id = models.AutoField(primary_key=True, blank=True)
    country = models.CharField(max_length=300, blank=True)
    about = models.CharField(max_length=300, blank=True)
    website_name = models.CharField(max_length = 200, blank=True) 

    def __str__(self):
        return str(self.user) 

class Cluster(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    cluster_name = models.CharField(max_length=200)
    cluster_desc = models.CharField(max_length=200, blank=True)
    cluster_hashtags = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.cluster_name    
 
# class Item(models.Model):
#     cluster = models.ForeignKey(Cluster,on_delete=models.CASCADE)
#     my_video = models.URLField()  # same like models.URLField()
    
#     def __str__(self):
#         return str(self.video)

class Video(models.Model):
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    video_platform_id = models.CharField(max_length=200)
    video_url = models.CharField(max_length=500)
    video_title = models.CharField(max_length=500, blank=True)
    video_description = models.CharField(max_length=2000, blank=True)
    video_thumbnail = models.CharField(max_length=500)
    video_owner_thumbnail = models.CharField(max_length=500, blank=True)
    video_owner = models.CharField(max_length=100)

    def __str__(self):
        return str(self.video_title)

