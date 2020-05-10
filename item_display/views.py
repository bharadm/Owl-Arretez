from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import auth
from django.views.generic.edit  import CreateView
from common.models import Product, User, UserCart
import ast

   
def index(request):
    id_value = str(request.GET.get('id'))
    product_details = Product.objects.get(ProductId = id_value)
    user_id = request.session.get("user")

    p_features = ast.literal_eval(product_details.ProductShortDesc)['features']
    p_extra_features = ast.literal_eval(product_details.ProductLongDesc)
    # p_qna = list(product_details.ProductQNA)
    p_qna = ast.literal_eval(product_details.ProductQNA)
    p_unr = ast.literal_eval(product_details.ProductUserReviews)
    return render(request, "item.html", {'user_id': user_id, 'prod_details' : product_details, 'features' : p_features, 'e_features' : p_extra_features, 'p_qna' : p_qna, 'p_unr' : p_unr})

def logout(request):
    auth.logout(request)
    return render(request, "user-details.html")


class Cart(CreateView):
    def get(self, request):
        id_value = request.GET['item_id']
        try:
            user_id = request.session.get("user")
            if not UserCart.objects.filter(userID= user_id).exists():
                UserCart.objects.create(userID= user_id, cartItems= {id_value : 1})
            else:
                cartObj = UserCart.objects.get(userID= user_id)
                cartIDs = ast.literal_eval(cartObj.cartItems)
                
                if id_value in cartIDs.keys():
                    cartIDs[id_value] = cartIDs[id_value] + 1
                else:
                    cartIDs[id_value] = 1
                
                UserCart.objects.update(cartItems= cartIDs)

            return JsonResponse({'result': True})
        except Exception as e:
            print (e)
            return JsonResponse({'result': False})

class GetCartCount(CreateView):
    def get(self, request):
        try:
            user_id = request.session.get("user")
            if UserCart.objects.filter(userID= user_id).exists():
                cartObj = UserCart.objects.get(userID= user_id)
                cartIDs = ast.literal_eval(cartObj.cartItems)
                value = 0
                for count in cartIDs.values():
                    value += int(count)
                return JsonResponse({'count' : value})
            else:
                return JsonResponse({'count' : 0})
        except Exception as e:
            print (e)
            return JsonResponse({'count' : 0})

class GetCartItems(CreateView):
    def get(self, request):
        tag_value = "<a class=\"list-group-item d-flex justify-content-between align-items-center\">\
                  {}\
                  <span class=\"badge badge-primary badge-pill\">{}</span>\
                </a> <a class=\"list-group-item d-flex justify-content-between align-items-center\" href=\"query/deletecart?itemid={}\">Delete</a>"
        user_id = request.session.get("user")
        try:
            if UserCart.objects.filter(userID= user_id).exists():
                cartObj = UserCart.objects.get(userID= user_id)
                cartIDs = ast.literal_eval(cartObj.cartItems)
                element = ""
                for key_item, value_item in cartIDs.items():
                    print (key_item, value_item)
                    if Product.objects.filter(ProductId = key_item).exists():
                        product_obj = Product.objects.get(ProductId = key_item)
                        element += tag_value.format("<br>(".join(str(product_obj.ProductName).split("(")),value_item, key_item)

                return JsonResponse({'status' : True, 'element' : element})
            else:
                return JsonResponse({'status' : False})
        except Exception as e:
            print (e)
            return JsonResponse({'status' : False})


def deleteItem(request):
    item_id = str(request.GET['itemid'])
    user_id = request.session.get("user")
    try:
        if UserCart.objects.filter(userID= user_id).exists():
            cartObj = UserCart.objects.get(userID= user_id)
            cartIDs = ast.literal_eval(cartObj.cartItems)
            if item_id in cartIDs.values():
                cartIDs[item_id] = int(cartIDs[item_id]) - 1
            print ("I am here ")
            UserCart.objects.filter(userID = user_id).update(cartItems = cartIDs)
            return render(request, "item.html",{'id': item_id})
        else:
            return render(request, "item.html",{'id': item_id})
    except:
        return render(request, "item.html",{'id': item_id})
            