from django.shortcuts import render
from django.http import HttpResponse 
from django.conf import settings
from stories.models import Category, Story
import re
from django.core.paginator import Paginator

# Create your views here.
def index(request): #home
    context = {}
    context['hello'] = 'Hello world!'
    context['title'] = 'Home page'
    context['STATIC_URL'] = settings.STATIC_URL
    context['image_story'] = ['mu1.jpg','mu2.jpg','mu3.jpg','mu4.jpg']
    context['categories'] = Category.objects.all()

    return render(request,'stories/index.html',context) 

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

    return render(request,'stories/category.html', context)

def story(request,pk): #story
    context = {}
    return render(request,'stories/story.html', context)

def contact(request): #contact
    context = {}
    return render(request, 'stories/contact.html', context)

def test(request): #test
      context = {}
      return render(request, 'stories/test.html', context)

def read_number(request, number = None):
    return HttpResponse("Value ... %d"%number)