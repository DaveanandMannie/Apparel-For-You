from django.shortcuts import render
# model imports
from .models import Item


def home(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, 'test.html', context)
