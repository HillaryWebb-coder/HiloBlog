from django.db import models
import sorl.thumbnail
from datetime import datetime

class Post(models.Model):
	title = models.CharField(max_length=255)
	content = models.TextField()
	image = sorl.thumbnail.ImageField(upload_to='uploads/')
	added = models.DateTimeField(default=datetime.now())
