from django.urls import path
from . import views

urlpatterns = [
    path('item', views.index, name ='Item page'), 
    path('query/addcart', views.Cart.as_view(), name= 'Add to cart'),
    path('query/getcart', views.GetCartCount.as_view(), name= 'Cart Count'),
    path('query/getcartitems', views.GetCartItems.as_view(), name= 'Cart Items'),
    path('query/deletecart', views.deleteItem, name = 'Delete cart item'),
    path('logout', views.logout, name= 'Logout user')
]
