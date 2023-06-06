from django.contrib import admin
from .models import Category,  SubCategory, Product

# nhìn thấy thông tin ở admin
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "thumbnail", "Category")

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "subcategory", "thumbnail")

# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin) 