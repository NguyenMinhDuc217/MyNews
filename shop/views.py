from django.shortcuts import render
from shop.models import Category, SubCategory, Product, Cart, Option, SKU
from django.conf import settings
from django.db.models import F, Count
from django.template.defaulttags import register
from django import template
import re
from django.core.paginator import Paginator
from django.utils.safestring import mark_safe
from django.http import HttpResponse
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import form
from django.core.mail import EmailMultiAlternatives
from MyNews.settings import EMAIL_HOST_USER
from django.shortcuts import redirect
import feedparser
import datetime
import json
from rest_framework import viewsets, permissions
from shop.serializers import ProductSerializer
from django.forms.models import model_to_dict
from django.core import serializers


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
    if not request.user.is_authenticated:
        return render(request, 'shop/login.html')
    
    context = {}
    categories = Category.objects.all() #danh mục để gắn lên header
    for cat in categories:
        cat.subcategories = SubCategory.objects.filter(Category=cat.id)
    context['categories'] = categories
    context['clatest'] = SubCategory.objects.latest('pk') #SubCategory mới nhất để gắn clatest.id lên header
    context['subcat_id'] = int(request.GET.get('subcat_id', 0))
    context['MEDIA_URL'] = settings.MEDIA_URL

    # Mỗi SKU chỉ hiển thị sản phẩm đầu tiên trong danh sách sản phẩm
    sku = SKU.objects.all()
    product_new = []
    if request.GET.get('keyword'):
        for s in sku:
            product_old = Product.objects.filter(name__contains = request.GET.get('keyword')).first()
            product_new.append(product_old.id)
        context['products'] = Product.objects.filter(pk__in=product_new).order_by('-quantity_purchased')[0:5]
    else:
        for s in sku:
            product_old = Product.objects.filter(sku_code = s.sku_code).first()
            product_new.append(product_old.id)
        context['products'] = Product.objects.filter(pk__in=product_new).order_by('-quantity_purchased')[0:5]

    context['keyword'] = request.GET.get('keyword')
    context['top_viewed'] = Product.objects.order_by('-viewed')[0:3]
    context['best_seller'] = Product.objects.annotate(price_diff = F('price') - F('priceOrg')).order_by('-price_diff')[0:3]
    context['on_sale'] = Product.objects.order_by('-public_day')[0:3]

    return render(request, 'shop/index.html', context)

def contact(request):
    context = {}
    return render(request,'shop/contact.html', context)

def search_form(request):
    context = {}
    categories = Category.objects.all() #danh mục để gắn lên header
    for cat in categories:
        cat.subcategories = SubCategory.objects.filter(Category=cat.id)
    context['categories'] = categories
    context['clatest'] = SubCategory.objects.latest('pk') #SubCategory mới nhất để gắn clatest.id lên header
    context['subcat_id'] = int(request.GET.get('subcat_id', 0))
    context['MEDIA_URL'] = settings.MEDIA_URL
    context['products'] = Product.objects.filter(name__contains = request.GET.get('keyword')).order_by('-quantity_purchased')[0:5]
    context['top_viewed'] = Product.objects.order_by('-viewed')[0:3]
    context['best_seller'] = Product.objects.annotate(price_diff = F('price') - F('priceOrg')).order_by('-price_diff')[0:3]
    context['on_sale'] = Product.objects.order_by('-public_day')[0:3]

    return render(request, 'shop/index.html', context)

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
    
    option = Option.objects.filter(sku_code = product.sku_code).values()
    option_mau = []
    option_kich_thuoc = []

    for op in option:
        if op['type'] == 'color':
            option_mau.append(op)

        if op['type'] == 'size':
            option_kich_thuoc.append(op)

    context['option'] = option
    context['option_mau'] = option_mau
    context['option_kich_thuoc'] = option_kich_thuoc
    context['product'] = product
    context['content'] = mark_safe(product.content)
    return render(request,'shop/product-quickview.html', context)

def product(request):
    context = {}
    context['product'] = Product.objects.all()
    context['range'] = range(1,6)
    return render(request,'shop/product.html', context)

def api_product(request):
    product = Product.objects.order_by('public_day')
    result_list = list(product.values('name','price', 'priceOrg', 'content', 'public_day', 'image', 'banner', 'viewed', 'subcategory_id', 'quantity_purchased', 'rate'))
    return HttpResponse(json.dumps(result_list, indent=4, sort_keys=True, default=str).encode('utf8'))

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
    group_sku_products = {}
    sku_code = []
    for cart in carts:
        cart.product = Product.objects.get(pk=cart.product_id)
        sku_code = cart.product.sku_code
        product_id = cart.product_id
        if sku_code not in group_sku_products:
            group_sku_products[sku_code] = {}
        group_sku_products[sku_code][product_id] = cart
        total += cart.product.price * cart.quantility
    
        

    print(carts)
    print('----------------------------')
    print(group_sku_products)
    context['total'] = total
    context['carts'] = group_sku_products
    context['products'] = group_sku_products
    return render(request,'shop/cart.html', context)

def add_to_cart(request):
    context = {}
    product = Product.objects.filter(sku_code = request.GET.get('sku_code')).filter(option1 = request.GET.get('color')).filter(option2 = request.GET.get('size')).first()
    quantity_new = request.GET.get('quantility')

    if product is None:
        context = {"status": "error"}
        json_object = json.dumps(context, indent = 4) 
        return HttpResponse(json_object, content_type="application/json")

    cartCurr = Cart.objects.filter(product_id = product.id).first()
    if cartCurr is None:
        cart = Cart(name = product.name, quantility = int(quantity_new), status = 2, product_id = product.id)
        cart.save()
    else:
        cart = Cart.objects.filter(product_id = product.id).update(quantility = cartCurr.quantility + int(quantity_new))
    
    context ={ 
        "status": "success",
    }
    json_object = json.dumps(context, indent = 4) 

    return HttpResponse(json_object, content_type="application/json")

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

def updateQuickViewProduct(request):
    context = {}
    sku_code_op = request.POST['sku_code']
    option_id_color = request.POST['option_id_color']
    option_id_size = request.POST['option_id_size']
    
    product = Product.objects.filter(sku_code = sku_code_op).filter(option1 = option_id_color).filter(option2 = option_id_size)

    pr_json = serializers.serialize('json', product)

    context1 ={ 
        "status": "success",
        "product": pr_json
    }

    json_object = json.dumps(context1)

    return HttpResponse(json_object, content_type="application/json")

def delete(request):
    context = {}
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

def sign_in(request):
    registered = False
    if request.method == "POST":
        form_user = form.UserForm(data = request.POST)
        form_por = form.UserProfileInfoForm(data = request.POST)
        if form_user.is_valid() and form_por.is_valid() and request.POST.get('password') == request.POST.get('confirm'):
            user = form_user.save()
            user.set_password(user.password)
            user.save()

            profile = form_por.save(commit=False)
            profile.user = user
            if 'image' in request.FILES:
                profile.image = request.FILES['image']
            profile.save()

            registered = True

            email_address = request.POST.get('email')
            subject = "Tài khoản của Quý khách tại Shop đã được tạo."
            message = "Hãy trải nghiệm việc mua sắm online với các thiết bị gia đình, dụng cụ nhà bếp. <br>Trân trọng."
            recepient = str(email_address)
            html_content = '<h2 style="color:blue"><i>Kính chào ' + request.POST.get('username') + ',</i></h2>' +'<p>Chào mừng quý khách đến với <strong>My Shop</strong> website.</p>' + '<h4 style="color:red">' + message + '</h4>'
            msg = EmailMultiAlternatives(subject, message, EMAIL_HOST_USER, [recepient])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

        if request.POST.get('password') != request.POST.get('confirm'):
            form_user.add_error(
                'confirm', 'Password và confirm password phải giống nhau!'
            )
            print(form_user.errors, form_por.errors)
    else:
        form_user = form.UserForm()
        form_por = form.UserProfileInfoForm()

    username = request.session.get('username', 0)
    context = {}
    context['form_user'] = form_user
    context['form_por'] = form_por
    context['username'] = username
    context['registered'] = registered
    return render(request, 'shop/sign-in.html', context)

def log_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            result = "Hello " + username
            request.session['username'] = username
            username = request.session.get('username', 0)
            return redirect('index.html')
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


# API
def read_feed(request):
    context={}
    NewsFeed = feedparser.parse("https://tuoitre.vn/rss/tin-moi-nhat.rss")
    entry = NewsFeed.entries
    context['today'] = datetime.datetime.now()
    img = []
    temp = []
    for e in entry:
        start_img = e.summary.find('<img')
        end_img = e.summary.rfind('/>')
        img = e.summary[0:end_img+6]

        sub_2 = e.summary[end_img+6:len(e.summary)]\
        
        data = {'title': e.title, 'summary': e.summary, 'sub_2': sub_2, 'image': img }
        temp.append(data)

    context['feeds'] = temp
    context['feeds_full'] = entry
    context['last_visit'] = request.session.get('last_visit',False)
    context['username'] = request.session.get('username',0)

    return render(request, 'shop/rss.html', context)

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-public_day')
    serializer_class = ProductSerializer 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



