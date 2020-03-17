from django.shortcuts import render

from common.models import Product

# Create your views here.

def home(request):

    product = Product()
    product.ProductName = "Iphone X"
    product.ProductShortDesc = "Iphone has the been made in china and manufactured in US."
    product.ProductPrice = "$ 999"

    product_list = [product]

    return render(request, "index.html", {'Product_list' : product_list})