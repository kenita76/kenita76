from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI 

#crea una instancia de NinjaAPI
api= NinjaAPI()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),  
]

