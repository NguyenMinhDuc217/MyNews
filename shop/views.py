from django.shortcuts import render
from shop.models import Category, SubCategory, Product, Cart
from django.conf import settings
from django.db.models import F
from django.template.defaulttags import register
from django import template
import re
from django.core.paginator import Paginator
from django.utils.safestring import mark_safe
from django.http import HttpResponse
import json
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_requireds

register = template.Library()
# HÀM TÍNH TOÁN
@register.filter
def subtract(value, arg):
    return value - arg

@register.filter(name='multiplication') # nhân
def multiplication(value, arg):
    return value * arg

# Create your views here.
def index(request):
    context = {}
    categories = Category.objects.all() #danh mục để gắn lên header
    for cat in categories:
        cat.subcategories = SubCategory.objects.filter(Category=cat.id)
    context['categories'] = categories
    context['clatest'] = SubCategory.objects.latest('pk') #SubCategory mới nhất để gắn clatest.id lên header
    context['subcat_id'] = int(request.GET.get('subcat_id', 0))
    context['MEDIA_URL'] = settings.MEDIA_URL
    context['products'] = Product.objects.order_by('-quantity_purchased')[0:5]
    context['top_viewed'] = Product.objects.order_by('-viewed')[0:3]
    context['best_seller'] = Product.objects.annotate(price_diff = F('price') - F('priceOrg')).order_by('-price_diff')[0:3]
    context['on_sale'] = Product.objects.order_by('-public_day')[0:3]

    return render(request, 'shop/index.html', context)

def contact(request):
    context = {}
    return render(request,'shop/contact.html', context)

def search_form(request):
    context = {}
    return render(request, 'shop/searchform.html', context)

def shopgrid(request, subcat_id):
    context = {}
    context['title'] = 'Shop grid'
    context['MEDIA_URL'] = settings.MEDIA_URL
    categories = Category.objects.all() #danh mục để gắn lên header
    for cat in categories:
        cat.subcategories = SubCategory.objects.filter(Category=cat.id)
    context['categories'] = categories #end danh mục để gắn lên header
    context['clatest'] = SubCategory.objects.latest('pk') #SubCategory mới nhất để gắn clatest.id lên header
    
    context['subcat_id'] = subcat_id
    context['search_sub_id'] = int(request.GET.get('subcat_id', 0))
    context['keyword'] = str(request.GET.get('keyword', ''))

    subcategory_current = SubCategory.objects.get(pk=subcat_id) #subcategory hiện tại
    context['subInfo'] = subcategory_current

    #paginator start
    pageStart = 1 #page phân trang bắt đầu
    pageLimit = 9 #số story trên 1 page phân trang
    
    product_list = Product.objects.filter(subcategory=subcat_id)
    for product in product_list:
        product.content = re.sub('<[^<]+?>','',product.content)
    page = request.GET.get('page',pageStart)
    paginator = Paginator(product_list, pageLimit)
    try:
        products = paginator.page(page)
    except PageNotAnInterger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    #paginator end
    
    context['products'] = products #sản phẩm thuộc danh mục hiện tại subcat_id
    context['items'] = products #dùng biến items để truyền sang template phân trang dùng chung
    context['newests'] = Product.objects.order_by("-public_day")[0:3] #4 sp mới ở shop_grid.html
    context['product'] = product_list.filter(id=subcat_id)

    return render(request,'shop/shop-grid.html', context)

def quickview(request, product_id):
    context = {}
    product = Product.objects.get(pk=product_id) #sp hiện tại)
    context['product'] = product
    context['content'] = mark_safe(product.content)
    return render(request,'shop/product-quickview.html', context)

def product(request):
    context = {}
    context['product'] = Product.objects.all()
    context['range'] = range(1,6)
    return render(request,'shop/product.html', context)

def product_detail(request, product_id):
    product_current = Product.objects.get(pk=product_id) #bài hiện tại
    Product.objects.filter(pk=product_current.pk).update(viewed = product_current.viewed+1)
    product_current.refresh_from_db()

    context = {}
    categories = Category.objects.all()
    for cat in categories:
        cat.subcategories = SubCategory.objects.filter(Category=cat.id)
    context['categories'] = categories

    context['clatest'] = SubCategory.objects.latest('pk') #SubCategory mới nhất để gắn clatest.id lên header
    context['subcat_id'] = int(request.GET.get('subcat_id', 0))
    context['search_sub_id'] = int(request.GET.get('subcat_id', 0))
    context['keyword'] = str(request.GET.get('keyword', ''))
    
    context['product'] = product_current #sp hiện tại
    
    context['range'] = range(1,6)
    return render(request,'shop/product-detail.html', context)

@register.filter(name='range')
def filter_range(start, end):
    return range(start, end)

def shopcart(request):
    context = {}
    carts = Cart.objects.filter(status=2)
    total = 0
    for cart in carts:
        cart.product = Product.objects.get(pk=cart.product_id)
        total += cart.product.price * cart.quantility
    
    context['total'] = total
    context['carts'] = carts
    context['carts_temp'] = list(carts)
    return render(request,'shop/cart.html', context)

def updateQuantility(request):
    context = {}
    cart = Cart.objects.get(pk = request.POST['id'])
    cart.quantility = request.POST['quantility']
    cart.save()

    context ={ 
        "status": "success",
    }
    json_object = json.dumps(context, indent = 4) 

    return HttpResponse(json_object, content_type="application/json")

def delete(request):
    context = {}
    print(1233333333333333333333333333333333333333333333333)
    print(request.POST['id'])
    cart = Cart.objects.get(pk = request.POST['id'])
    cart.status = 0
    cart.save()

    context = {
        "status": "success",
    }

    json_object = json.dumps(context, indent=4)
    return HttpResponse(json_object, content_type="application/json")

def checkout(request):
    context = {}
    return render(request,'shop/checkout.html', context)

def login(request):
    if request.method == "POST":
        username = request.post.get('username')
        password = request.post.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            result = "Hello " + username
            request.session['username'] = username
            username = request.session.get('username', 0)
            return render(request, 'shop/login.html', {'login_result': result, 'username': username})
        else:
            print("you can't login. ")
            print("Username: {} and password: {}".format(username, password))
            login_result = "Username hoặc password không chính xác"
            return render(request, 'shop/login.html', {'login_result': login_result})
    else:
        return render(request, 'shop/login.html')
    
@login_required
def log_out(request):
    logout(request)
    result = "Quý khách đã logout. Quý khách có thể login trở lại"
    return render(request, "shop/login.html", {'logout_result': result})