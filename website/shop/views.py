from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Item


def home(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, 'main.html', context)

def profile(request, pk):
    user = User.objects.get(id=pk)