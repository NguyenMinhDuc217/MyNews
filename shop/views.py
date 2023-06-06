from django.shortcuts import render
from shop.models import Category, SubCategory, Product
from django.conf import settings
from django.db.models import F
from django.template.defaulttags import register
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
    context['best_seller'] = Product.objects.annotate(price_diff = F('price') - F('priceOrg')).order_by('-price_diff') 
    
    print(context['best_seller'])

    return render(request, 'shop/index.html', context)

@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg

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