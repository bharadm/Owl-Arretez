from django.shortcuts import render
from common.models import Product

from django.views.generic.edit  import CreateView
from django.http import JsonResponse
# Create your views here.
def list(request):
    #category_value = request.GET.get('c')
    product_list = Product.objects.all()
    return render(request, "item-list.html", {'product_list' : product_list})
