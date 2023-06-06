from django.shortcuts import render
from django.http import HttpResponse 
from django.conf import settings
from stories.models import Category, Story
import re
from django.core.paginator import Paginator
import datetime

# Create your views here.
def index(request):
    context ={}

    story_list = Story.objects.order_by("-public_day") #
    context['title'] = 'Home page' #title trên base.html/header 
    context['MEDIA_URL'] = settings.MEDIA_URL #
    context['today'] = datetime.datetime.now() #thời gian trên header
    context['latest'] = Story.objects.latest('pk') #bài mới nhất để gắn latest.id lên header
    context['categories'] = Category.objects.all() #danh mục để gắn lên header

    context['first'] =  story_list[0] #ảnh đầu tiên trên slide show
    context['next4s'] = story_list[1:5] #4 ảnh kế trên slide show
    context['newest'] = Story.objects.order_by("-public_day")[0:4] #4 bài mới ở footer

    context['cat_id'] = 0 # bổ sung để gắn active cho menu navigation, mặc định = 0
    context['story_id'] = 0 # bổ sung để gắn active cho menu navigation, mặc định = 0
   
    return render(request,'stories/index.html', context)

def category(request, cat_id): #category
    context = {}

    pageStart = 1 #page phân trang bắt đầu
    pageLimit = 2 #số story trên 1 page phân trang
    story_list = Story.objects.filter(category = cat_id)
    for story in story_list:
        story.content = re.sub('<[^<]+?>','',story.content)
    
    page = request.GET.get('page',pageStart)
    paginator = Paginator(story_list, pageLimit)
    try:
        stories = paginator.page(page)
    except PageNotAnInterger:
        stories = paginator.page(1)
    except EmptyPage:
        stories = paginator.page(paginator.num_pages)

       
    category_current = Category.objects.get(pk = cat_id)
    context['categories'] = Category.objects.all()
    context['category'] = category_current
    context['stories'] = stories
    context['items'] = stories
    context['MEDIA_URL'] = settings.MEDIA_URL
    context['today'] = datetime.datetime.now()
    context['latest'] = Story.objects.latest('pk') #bài mới nhất để gắn latest.id lên header
    context['newest'] = Story.objects.filter(category=cat_id).order_by("-public_day")[0:4] #4 bài mới ở footer


    return render(request,'stories/category.html', context)

def story(request,story_id):
    story_current = Story.objects.get(pk=story_id) #bài hiện tại)
    context = {}
    context['title'] = story_current.name #title trên base.html/header 
    context['MEDIA_URL'] = settings.MEDIA_URL
    context['today'] = datetime.datetime.now() #thời gian trên header
    context['latest'] = Story.objects.latest('pk') #bài mới nhất để gắn latest.id lên header
    context['categories'] = Category.objects.all() #category trên thanh menu
    context['newest'] = Story.objects.order_by("-public_day")[0:4] #4 bài mới ở footer
    context['story'] = story_current #bài hiện tại
    context['stories'] = Story.objects.filter(category=story_current.category).order_by("-public_day") #bài liên quan
    context['cat_id'] = 0 # bổ sung để gắn active cho menu navigation, mặc định = 0
    context['story_id'] = story_id # bổ sung để gắn active cho menu navigation
 
    return render(request,'stories/story.html', context)

def contact(request): #contact
    context = {}
    print(request)
    context['cat_id'] = 0 
    context['story_id'] = 0 
    context['today'] = datetime.datetime.now()
    context['MEDIA_URL'] = settings.MEDIA_URL
    context['categories'] = Category.objects.all()
    context['latest'] = Story.objects.latest('pk') #bài mới nhất để gắn latest.id lên header
    context['newest'] = Story.objects.order_by("-public_day")[0:4] #4 bài mới ở footer

    return render(request, 'stories/contact.html', context)

def test(request): #test
      context = {}
      return render(request, 'stories/test.html', context)

def read_number(request, number = None):
    return HttpResponse("Value ... %d"%number)