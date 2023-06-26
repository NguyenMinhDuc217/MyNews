from django.urls import path, re_path
from . import views
from django.views import View
app_name = "shop"
urlpatterns = [
    path('',views.index, name="index.html"),
    path('index.html', views.index, name='index.html'),
    path('contact.html', views.contact, name='contact.html'),
    path('search_form.html', views.search_form, name='search_form.html'),
    path('shop-grid.html/<int:subcat_id>', views.shopgrid, name='shop-grid.html'),
    path('product.html', views.product, name='product.html'),
    path('product-quickview.html/<int:product_id>', views.quickview, name='product-quickview.html'),
    path('product-detail.html/<int:product_id>', views.product_detail, name='product-detail.html'),
    path('cart.html', views.shopcart, name='cart.html'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('updateQuantility', views.updateQuantility, name="updateQuantility"),
    path('updateQuickViewProduct', views.updateQuickViewProduct, name="updateQuickViewProduct"),
    path('delete', views.checkout, name="delete"),
    path('checkout.html', views.checkout, name='checkout.html'),
    path('login.html', views.log_in, name='login.html'),
    path('logout.html', views.log_out, name='logout'),
    path('sign-in.html', views.sign_in, name='sign-in.html'),
    path('read_feed', views.read_feed, name='read_feed'),

    path('api_product', views.api_product, name='api_product'),

    
]