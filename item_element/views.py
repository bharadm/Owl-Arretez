from django.shortcuts import render

# Create your views here.
def retrieve_item(request):

    return render(request, "element.html")