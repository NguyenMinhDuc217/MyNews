from django.db import models
import datetime
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = RichTextUploadingField(default="")

    def __str__(self):
        return self.name
    
class Story(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=150, unique=True)
    author = models.CharField(max_length=250)
    url = models.URLField(null=True)
    content = models.TextField()
    public_day = models.DateField(default=datetime.date.today)
    image = models.ImageField(upload_to="static/images", default="static/images/default.jpg")

    def __str__(self):
        return self.name

