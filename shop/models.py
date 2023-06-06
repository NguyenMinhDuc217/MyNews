from django.db import models
from django.utils.html import mark_safe #dùng tạo thumbnail
from ckeditor_uploader.fields import RichTextUploadingField
import datetime

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to ="shop_media/category/", default ="shop_media/default.png")
    def thumbnail(self): 
        return mark_safe(f'<img class="img-thumbnail" src = "{self.image.url}" width = "100"/>')
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    Category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to ="shop_media/category/", default ="shop_media/default.png")
    def thumbnail(self): 
        return mark_safe(f'<img class="img-thumbnail" src = "{self.image.url}" width = "100"/>')
    def __str__(self):
        return self.name

class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    name = models.CharField(max_length=150, unique=True)
    price = models.FloatField(default=0.0)
    priceOrg = models.FloatField(null=True)
    content = RichTextUploadingField()
    public_day = models.DateField(default=datetime.date.today)
    image = models.ImageField(upload_to ="shop_media/product/", default ="shop_media/default.png")
    banner = models.ImageField(upload_to ="shop_media/product/", default ="shop_media/default.png")
    viewed = models.IntegerField(default=0)
    quantity_purchased = models.IntegerField(default=0)

    def thumbnail(self): 
        return mark_safe(f'<img class="img-thumbnail" src = "{self.image.url}" width = "100"/>')
    def __str__(self):
        return self.name
    