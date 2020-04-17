from django.shortcuts import render, redirect
#from common.models import User
from django.contrib.auth.models import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.edit  import CreateView
from django.http import JsonResponse
# Create your views here.

import math, random
def home(request):
    return render(request, "user-details.html")

def generateOTP() : 
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = "" 
    length = len(string) 
    for i in range(5) : 
        OTP += string[math.floor(random.random() * length)] 
    
    return OTP 

class UserLogin(CreateView):
    def get(self, request):
        data_taken = {}
        username = request.GET['username']
        password = request.GET['password']
        try:
            print (username, password)
            userDetails = auth.authenticate(username = username, password= password)
            if userDetails is not None:
                auth.login(request, userDetails)
                request.session["user"] = userDetails.id
                data_taken = {
                'is_taken' : True
                }
        except Exception as e:
            print ("Exception is ", e)
            data_taken = {
                'is_taken' : False
            }
        return JsonResponse(data_taken)

           
# Create your views here.
class UserRegistration(CreateView):
 
# Create your views here.
    def get(self, request):
        username = request.GET.get('firstname')
        lastname = request.GET.get('lastname')
        email = request.GET.get('email')
        password = request.GET.get('password')
        #verification_code = generateOTP()
        try:
            userDetails = User.objects.create_user(first_name = username, last_name = lastname, username = email, password = password)
            userDetails.save()
            data = {
                'is_taken' : True
            }
            
        except:
            data = {
                'is_taken' : False
            }
        return JsonResponse(data)
