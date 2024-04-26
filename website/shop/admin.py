from django.contrib import admin
from .models import ShoeSize, ClothingSize, Category, Brand, ProductLine, Item, UserAddress

admin.site.register(ShoeSize)
admin.site.register(ClothingSize)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductLine)
admin.site.register(Item)
admin.site.register(UserAddress)
