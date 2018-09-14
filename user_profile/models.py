from django.db import models
from django.contrib.auth.models import User
import os
from user_details import settings
from django.utils import timezone

# Create your models here.
class Profile_detail(models.Model) :
	profile_image = models.ImageField(upload_to = 'image_uploads', null= True, blank = True)
	DOB = models.DateField(auto_now = False, blank = False)
	address = models.CharField(max_length = 100, blank = False)
	username = models.OneToOneField(User)


class Blog(models.Model):
	title = models.CharField(max_length = 100, blank = False)
	Description = models.CharField(max_length = 1000, blank = False )
	create_date = models.DateTimeField(editable = False)
	last_updated = models.DateTimeField()
	publisher = models.ForeignKey(User, related_name = 'blogs')


	def save(self,*args,**kwargs):
		if not self.id:
			self.create_date = timezone.now()
		self.last_updated = timezone.now()
		return super(Blog,self).save(*args,**kwargs)

class Like(models.Model):
	user = models.ForeignKey(User, related_name = 'likes')
	blog = models.ForeignKey(Blog, related_name = 'likes')