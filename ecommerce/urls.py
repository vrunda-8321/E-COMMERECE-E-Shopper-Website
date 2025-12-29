from django.urls import path
from .views import index,cart,checkout,contact,detail,shop,login,logout,register
from . import views

urlpatterns = [
    
    path('',index,name='index'),
    # path('cart/',cart,name='cart'),
    path('checkout/',checkout,name='checkout'),
    path('contact/',contact,name='contact'),
    path('detail/',detail,name='detail'),
    path('shop/',shop,name='shop'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('register/',register,name='register'),


    path("products/",views.product_list,name='product_list'),
    path("products/add/",views.add_product,name='add_product'),
    path("products/edit/<int:pid>/",views.edit_product,name='edit_product'),
    path("products/delete/<int:pid>/",views.delete_product,name='delete_product'),
    
    
    

    path('shop/', views.shop, name='shop'),
    path('add-to-cart/<int:pid>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_page, name='cart_page'),
    path('decrease-qty/<int:pid>/', views.decrease_qty, name='decrease_qty'),
    path('increase-qty/<int:pid>/', views.increase_qty, name='increase_qty'),
    path('remove-item/<int:pid>/', views.remove_item, name='remove_item'),
    path('checkout/', views.checkout_page, name='checkout_page'),
    path('place-order/', views.place_order, name='place_order'),



]
