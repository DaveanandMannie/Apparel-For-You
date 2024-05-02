from django.contrib import admin
from django.urls import path, include

# TODO: Create a landing page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls'))
]
