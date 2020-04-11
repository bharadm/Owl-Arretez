from django.urls import path
from . import views

urlpatterns = [
    path('item-details', views.list, name ='Items list'),
]
