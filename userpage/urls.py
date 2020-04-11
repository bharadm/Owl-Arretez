from django.urls import path
from . import views

urlpatterns = [
    path('login', views.home, name ='User Page'),
    path('query/signin', views.UserLogin.as_view(), name ='Signing in'),
    path('query/signup', views.UserRegistration.as_view(), name ='registration'),
]
