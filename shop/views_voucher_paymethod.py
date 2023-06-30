from django.shortcuts import render
from shop.models import Category, SubCategory, Product, Cart, Option, SKU, Voucher
from django.conf import settings

def voucher(request):
    context = {}
    vouchers = Voucher.objects.all()
    context['vouchers'] = vouchers
    return render(request,'cart.html',context)