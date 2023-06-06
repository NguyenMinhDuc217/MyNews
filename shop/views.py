from django.shortcuts import render

# Create your views here.
def index(request):
    context = {}
    return render(request, 'shop/index.html', context)

def contact(request):
    context = {}
    return render(request,'shop/contact.html', context)

def shopgrid(request):
    context = {}
    return render(request,'shop/shopgrid.html', context)

def product(request):
    context = {}
    return render(request,'shop/product.html', context)

def shopcart(request):
    context = {}
    return render(request,'shop/shopcart.html', context)

def checkout(request):
    context = {}
    return render(request,'shop/checkout.html', context)