from django.urls import path,re_path 
from . import views 
app_name = "stories"
urlpatterns = [ 
	path('index', views.index, name='index'),
    path('read_number/<int:number>', views.read_number, name='read_number'),
    path('category/<int:cat_id>',views.category, name='category'),
    path('story',views.story, name='story'),
    path('contact',views.contact, name='contact'),
    path('test',views.test, name='test'),
] 
