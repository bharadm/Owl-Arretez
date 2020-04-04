from django.shortcuts import render
from common.models import Product

import ast

# Create your views here.
def index(request):
    id_value = str(request.GET['id'])
    product_details = Product.objects.get(ProductId = id_value)
    p_features = ast.literal_eval(product_details.ProductShortDesc)['features']
    p_extra_features = ast.literal_eval(product_details.ProductLongDesc)
    # p_qna = list(product_details.ProductQNA)
    p_qna = ast.literal_eval(product_details.ProductQNA)
    return render(request, "item.html", {'prod_details' : product_details, 'features' : p_features, 'e_features' : p_extra_features, 'p_qna' : p_qna})