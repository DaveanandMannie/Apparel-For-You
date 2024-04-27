from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import QuerySet, Q
from .models import Item, ProductLine, UserAddress, UserCart, CartItem, Brand, Category
from .forms import UserForm, AddressForm
from decimal import Decimal
from django_htmx.middleware import HtmxDetails


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


def search(request: HtmxHttpRequest) -> HttpResponse:
    items: list = []
    query: str = request.GET.get(key='query', default='')
    query_placeholder: str = query
    product_lines = ProductLine.objects.filter(
        Q(item__color__icontains=query) |
        Q(name__icontains=query) |
        Q(brand__name__icontains=query) |
        Q(categories__name__icontains=query)
    ).distinct()
    for product_line in product_lines:
        first_item = Item.objects.filter(product_line=product_line).first()
        items.append(first_item)
    context: dict = {
        'items': items,
        'query_placeholder': query_placeholder
    }

    return render(request, 'shop/_search.html', context)


def home(request: HttpRequest) -> HttpResponse:
    brands: Brand = Brand.objects.all()
    categories: Category = Category.objects.all()
    items: list = []
    # query
    query = request.GET.get(key='query', default='')
    query_placeholder = query
    product_lines = ProductLine.objects.filter(
        Q(item__color__icontains=query) |
        Q(name__icontains=query) |
        Q(brand__name__icontains=query) |
        Q(categories__name__icontains=query)
    ).distinct()

    for product_line in product_lines:
        first_item = Item.objects.filter(product_line=product_line).first()
        items.append(first_item)
    # quick cart
    if request.user.is_authenticated:
        user = request.user
        user_cart, created = UserCart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(user_cart=user_cart)
    else:
        cart_items = None
        user_cart = None
    context: dict = {
        'items': items,
        'brands': brands,
        'categories': categories,
        'cart_items': cart_items,
        'user_cart': user_cart,
        'query_placeholder': query_placeholder,
    }
    return render(request, 'shop/home.html', context)


def itemPage(request: HttpRequest, pk: int) -> HttpResponse:
    product: ProductLine = ProductLine.objects.get(id=pk)
    items: QuerySet = Item.objects.filter(product_line=product)
    first_item: Item = items.first()
    # quick cart
    if request.user.is_authenticated:
        user = request.user
        user_cart, created = UserCart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(user_cart=user_cart)
    else:
        cart_items = None
        user_cart = None
    context: dict = {
        'product': product,
        'items': items,
        'first_item': first_item,
        'cart_items': cart_items,
        'user_cart': user_cart
    }
    return render(request, 'shop/itemPage.html', context)


# ------------------------ User account start -------------------- #
def loginPage(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            username = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
        except User.DoesNotExist:
            messages.error(request, 'Incorrect username')
            return redirect(request.META.get('HTTP_REFERER'))

        if user is not None:
            login(request, user)
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Incorrect password')
    return render(request, 'shop/login.html')


@login_required(login_url='login')
def logoutUser(request: HttpRequest) -> HttpRequest:
    logout(request)
    return redirect('home')


def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Please check your entries.')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'shop/register.html', context)


@login_required(login_url='login')
def profile(request: HttpRequest, pk: int) -> HttpResponse:
    user: User = User.objects.get(id=pk)
    user_form = UserForm(instance=user)
    address, created = UserAddress.objects.get_or_create(user=user)
    address_form = AddressForm(instance=address)
    # move to separate url
    if request.method == 'POST':
        if 'user_submit' in request.POST:
            user_form = UserForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
        elif 'address_submit' in request.POST:
            address_form = AddressForm(request.POST, instance=address)
            if address_form.is_valid():
                if address:
                    address_form.save()
    context: dict = {
        'user': user,
        'user_form': user_form,
        'address_form': address_form,
    }
    return render(request, 'shop/profile.html', context)


def testUser(request: HttpRequest) -> HttpResponse:
    user = authenticate(request, username='jane', password='testtest123')
    if user is not None:
        login(request, user)
        return redirect('home')
    messages.error(request, 'Test user has not been implemented')
    return redirect(request.META.get('HTTP_REFERER'))


# ------------------------ User account end --------------------- #
# ------------------------ User cart start --------------------- #
@login_required(login_url='login')
def removeCartItem(request: HttpRequest, cart_item_id: int) -> HttpResponse:
    cart_item = CartItem.objects.get(pk=cart_item_id)
    cart_item.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def updateCartItem(request: HttpRequest, cart_item_id: int) -> HttpResponse:
    if request.method != 'POST':
        return redirect(request.META.get('HTTP_REFERER'))
    cart_item: CartItem = CartItem.objects.get(pk=cart_item_id)
    new_quantity = request.POST.get(key='new_quantity', default='1')
    if int(new_quantity) < 1:
        cart_item.delete()
    else:
        cart_item.quantity = new_quantity
        cart_item.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def addToCart(request: HttpRequest) -> HttpResponse:
    user = request.user
    user_cart, created = UserCart.objects.get_or_create(user=user)
    size = request.POST.get('size')
    color_id = request.POST.get('color_id')

    item = Item.objects.get(pk=color_id)
    amount = int(request.POST.get('item_quantity'))
    if not size or not color_id:
        messages.error(request, 'Please select size and colour')
        return redirect(request.META.get('HTTP_REFERER'))
    existing_cart_item: CartItem = CartItem.objects.filter(
        user_cart=user_cart,
        item=item,
        quantity=amount,
        size=size
    ).first()
    if existing_cart_item:
        existing_cart_item.quantity += amount
        existing_cart_item.save()
    else:
        CartItem.objects.create(
            user_cart=user_cart,
            item=item,
            quantity=amount,
            size=size
        )
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def viewCart(request: HttpRequest) -> HttpResponse:
    user = request.user
    user_cart, created = UserCart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(user_cart=user_cart)
    if request.method == 'POST':
        item_id = request.POST['item']
        new_quantity: int = int(request.POST.get(key='new_quantity', default='1'))
        if new_quantity < 1:
            cart_item = CartItem.objects.get(user_cart=user_cart, item_id=item_id)
            cart_item.delete()
        else:
            cart_item = CartItem.objects.get(user_cart=user_cart, item_id=item_id)
            cart_item.quantity = new_quantity
            cart_item.save()
        return redirect(request.META.get('HTTP_REFERER'))
    tax: Decimal = Decimal('0.13')
    total: Decimal = user_cart.total()
    tax_amount: Decimal = round(total * tax, 2)
    final_total: Decimal = round(total + tax_amount, 2)
    context: dict = {
        'cart_items': cart_items,
        'user_cart': user_cart,
        'tax_amount': tax_amount,
        'final_total': final_total
    }
    for cart_item in context['cart_items']:
        cart_item.per_item_price = cart_item.item.price * cart_item.quantity
    return render(request, 'shop/userCart.html', context)
# ------------------------ User cart end ----------------------- #
