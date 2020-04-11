from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('index', include('index_page.urls')),
    path('admin/', admin.site.urls),
    path('item', include('item_display.urls')),
    path('', include('item_list.urls')),
    path('', include('userpage.urls')),
    # path('query/signup', include('item_list.urls')),
    # path('item-details', include('item_list.urls')),
]
