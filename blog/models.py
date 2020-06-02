from django.db import models
import sorl.thumbnail
from datetime import datetime
from django.contrib.auth.models import User

superuser = User.objects.filter(is_superuser=True)

class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, default=superuser[0].id)
	title = models.CharField(max_length=255)
	content = models.TextField()
	excerpt = models.TextField(max_length=500, null=True)
	image = sorl.thumbnail.ImageField(upload_to='uploads/')
	added = models.DateTimeField(default=datetime.now())


class Profile(models.Model):
	author = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	firstname = models.CharField(max_length=255)
	lastname = models.CharField(max_length=255)
	email = models.EmailField(max_length=255)
	avatar = sorl.thumbnail.ImageField(upload_to='uploads/profiles')
