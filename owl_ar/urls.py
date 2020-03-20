
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('index', include('index_page.urls')),
    path('admin/', admin.site.urls),
    path('item', include('item_display.urls'))
]
