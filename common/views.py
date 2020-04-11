from django.shortcuts import render
from models import User
from django.http import JsonResponse

# Create your views here.
def signin(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    try:
        userDetails = User.objects.filter(UserEmail_iexact = username, UserPassword_iexact = password).exist()
        data = {
            'is_taken' : userDetails
        }
    except:
        data = {
            'is_taken' : False
        }
    return JsonResponse(data)

def signup(request):
    username = request.POST.get('firstname', None)
    lastname = request.POST.get('lastname', None)
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)

    try:
        userDetails = User.objects.create(UserFirstName = username, UserLastName = lastname, UserEmail = email, UserPassword = password)
        data = {
            'is_taken' : True
        }
    except:
        data = {
            'is_taken' : False
        }
    return JsonResponse(data)