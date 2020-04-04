from django.shortcuts import render
from common.models import Product

# Create your views here.
def list(request):
    category_value = request.GET['c']
    product_list = Product.objects.all()
    return render(request, "item-list.html", {'product_list' : product_list})