from django.shortcuts import render
from common.models import User

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
            username = request.GET.get('username')
            password = request.GET.get('password')
            try:
                userDetails = User.objects.filter(UserEmail = username, UserPassword= password).exists()
                data = {
                    'is_taken' : True
                }
            except:
                data = {
                    'is_taken' : False
                }
            return JsonResponse(data)


# Create your views here.
class UserRegistration(CreateView):
 
# Create your views here.
    def get(self, request):
        username = request.GET.get('firstname')
        lastname = request.GET.get('lastname')
        email = request.GET.get('email')
        password = request.GET.get('password')
        verification_code = generateOTP()
        try:
            userDetails = User.objects.create(UserFirstName = username, UserLastName = lastname, UserEmail = email, UserPassword = password, UserVerificationCode = verification_code)
            data = {
                'is_taken' : True,
                'verificationCode' : verification_code
            }
        except:
            data = {
                'is_taken' : False
            }
        return JsonResponse(data)