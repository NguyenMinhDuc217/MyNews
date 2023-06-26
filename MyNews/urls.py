"""
URL configuration for MyNews project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers
from shop import views as shopviews
from stories import views as storyviews

router = routers.DefaultRouter()
router.register(r'shop',shopviews.ShopViewSet)
router.register(r'stories',storyviews.StoryViewSet)

urlpatterns = [
    path('', include('shop.urls', namespace="shop")),
    path('admin/', admin.site.urls),
    path('stories/', include('stories.urls')),
    # path('shop/', include('shop.urls')),
    re_path(r'^ckeditor/',include('ckeditor_uploader.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'api/', include(router.urls)),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

