from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('animals.urls')),
]
from django.conf import settings
from django.conf.urls.static import static
