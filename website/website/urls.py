from django.contrib import admin
from django.urls import path, include
from shop.views import landing, diagram
# TODO: Create a landing page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls')),
    path('', landing, name='landing'),
    path('_diagram/', diagram, name='diagram'),
]
