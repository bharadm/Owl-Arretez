from django.urls import path
from . import views

urlpatterns = [
    path('item', views.index, name ='Item page'), 
    path('query/addcart', views.Cart.as_view(), name= 'Add to cart'),
    path('query/getcart', views.GetCartCount.as_view(), name= 'Cart Count')
]
