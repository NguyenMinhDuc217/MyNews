from django.db import models
from django.utils.html import mark_safe #dùng tạo thumbnail
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
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
    rate = models.FloatField(default=0)

    def thumbnail(self): 
        return mark_safe(f'<img class="img-thumbnail" src = "{self.image.url}" width = "100"/>')
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    name = models.CharField(max_length=150, unique=True)
    quantility = models.IntegerField(default=0)
    description = RichTextUploadingField()

    ORDER_STATUS = [(0, 'failed'), (1, 'success'), (2, 'wait')]
    status = models.IntegerField(choices=ORDER_STATUS)

    def __str__(self):
        return self.name
    
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    address = models.CharField(max_length=250, unique=True)
    phoneNumber = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to ="shop_media/customer/", default ="shop_media/default.png")
    def thumbnail(self): 
        return mark_safe(f'<img class="img-thumbnail" src = "{self.image.url}" width = "100"/>')
    def str(self):
        return self.user.username