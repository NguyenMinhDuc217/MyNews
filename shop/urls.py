from django.urls import path, re_path
from . import views
app_name = "shop"
urlpatterns = [
    path('',views.index, name="index.html"),
    path('index.html', views.index, name='index.html'),
    path('contact.html', views.contact, name='contact.html'),
    path('shop-grid.html', views.shopgrid, name='shop-grid.html'),
    path('product.html', views.product, name='product.html'),
    path('cart.html', views.shopcart, name='cart.html'),
    path('checkout.html', views.checkout, name='checkout.html'),
]
