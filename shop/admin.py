from django.contrib import admin
from django.contrib.auth.models import User
from .models import Category,  SubCategory, Product, Cart, UserProfileInfo, Option, SKU, Voucher, PayMethod
import datetime

def change_public_day(modelAdmin, request, queryset):
    queryset.update(public_day = datetime.date.today())

change_public_day.short_description = "ABCDEF"
# nhìn thấy thông tin ở admin
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "thumbnail", "Category")

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "subcategory", "thumbnail")

class StoryA(admin.ModelAdmin):
    exclude = ('pay_method',)
    list_filter = ('name',)
    search_fields = ('name__contains',)
    actions = [change_public_day]

# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin) 
admin.site.register(Cart)
admin.site.register(UserProfileInfo)
admin.site.register(Option)
admin.site.register(SKU)
admin.site.register(Voucher, StoryA)
admin.site.register(PayMethod)


admin.site.site_header = "APP NEW"
