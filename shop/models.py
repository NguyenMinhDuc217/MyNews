from django.db import models
from django.utils.html import mark_safe #dùng tạo thumbnail
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
import datetime
from typing import List
from pydantic import BaseModel
from django.utils import timezone


class SKU(models.Model):
    name = models.CharField(max_length=150, default='SKU')
    sku_code = models.CharField(max_length=150, default='sku')

    def __str__(self):
        return self.name

class Option(models.Model):
    sku_code = models.CharField(max_length=150, default='sku')
    name = models.CharField(max_length=150)
    value = models.CharField(max_length=150, blank=True)
    type = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.name

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
    subcategory = models.ForeignKey(SubCategory, related_name='%(class)subcategory', on_delete=models.PROTECT)
    option1 = models.IntegerField(default=0)
    option2 = models.IntegerField(default=0)
    option3 = models.IntegerField(default=0)
    sku_code = models.CharField(max_length=150, default='sku')
    name = models.CharField(max_length=150)
    price = models.FloatField(default=0.0)
    priceOrg = models.FloatField(null=True)
    content = RichTextUploadingField()
    viewed = models.IntegerField(default=0)
    quantity_remaining = models.IntegerField(default=0)
    quantity_purchased = models.IntegerField(default=0)
    public_day = models.DateField(default=datetime.date.today)
    image = models.ImageField(upload_to ="shop_media/product/", default ="shop_media/default.png")
    banner = models.ImageField(upload_to ="shop_media/product/", default ="shop_media/default.png")
    rate = models.FloatField(default=0)
                             
    def thumbnail(self): 
        return mark_safe(f'<img class="img-thumbnail" src = "{self.image.url}" width = "100"/>')
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    name = models.CharField(max_length=150)
    quantility = models.IntegerField(default=0)
    description = RichTextUploadingField()

    ORDER_STATUS = [(0, 'failed'), (1, 'success'), (2, 'wait')]
    status = models.IntegerField(choices=ORDER_STATUS)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.name
    
class UserProfileInfo(models.Model):
    # Create relationship from this class to User
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    # Add any more  attribute you want
    address = models.CharField(max_length=250, unique=True)
    phoneNumber = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to ="shop_media/customer/", default ="shop_media/default.png")

    def thumbnail(self): 
        return mark_safe(f'<img class="img-thumbnail" src = "{self.image.url}" width = "100"/>')
    def str(self):
        return self.user.username

# class CustomDateTimeField(models.DateTimeField):
#     def value_to_string(self, obj):
#         val = self.value_from_object(obj)
#         if val:
#             val.replace(microsecond=0)
#             return val.isoformat()
#         return ''
class Voucher(models.Model):
    product_id = models.IntegerField(default=0)
    name = models.CharField(max_length=150)
    value = models.CharField(max_length=150)
    type = models.CharField(max_length=150)
    # day_start = CustomDateTimeField(auto_now_add=True)
    # day_end = CustomDateTimeField(auto_now_add=True)
    day_start = models.DateTimeField(default=timezone.now)
    day_end = models.DateTimeField(default=timezone.now)
    pay_method = models.CharField(max_length=150)
    ORDER_STATUS = [(0, 'failed'), (1, 'success'), (2, 'wait')]
    status = models.IntegerField(choices=ORDER_STATUS)

    def __str__(self):
        return self.name
    
class PayMethod(models.Model):
    namecode = models.CharField(max_length=150)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
