from django.db.models import (Model, CharField, DecimalField, IntegerField, TextField, ImageField, ForeignKey, CASCADE,
                              ManyToManyField)
from django.contrib.auth.models import User
from decimal import Decimal
from PIL import Image


class ShoeSize(Model):
    size = DecimalField(max_digits=3, decimal_places=1, unique=True)

    def __str__(self):
        return f'{self.size}'


class ClothingSize(Model):
    size = CharField(max_length=4, unique=True)

    def __str__(self):
        return self.size


class Category(Model):
    name = CharField(max_length=100)

    def __str__(self):
        return self.name


class Brand(Model):
    name = CharField(max_length=100, unique=True)

    def path(self, filename: str) -> str:
        return f'static/BrandPhotos/{self.name}/{filename}'

    photo = ImageField(upload_to=path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            new_size = (840, 840)
            img.thumbnail(new_size)
            img.save(self.photo.path)

    def __str__(self):
        return self.name


class ProductLine(Model):
    """
    Table for over arching item. ie: air forces
    """
    name = CharField(max_length=100)
    # TODO: figure out if I should use 'related_name' arg
    brand = ForeignKey(to=Brand, on_delete=CASCADE)
    categories = ManyToManyField(to=Category)
    description = TextField()

    def __str__(self):
        return self.name


class Item(Model):
    """
    handles the item colour and image fields
    """
    color = CharField(max_length=100)
    price = DecimalField(max_digits=10, decimal_places=2)
    product_line = ForeignKey(to=ProductLine, on_delete=CASCADE)
    shoe_size = ManyToManyField(to=ShoeSize, blank=True)
    clothing_size = ManyToManyField(to=ClothingSize, blank=True)

    def path(self, filename: str) -> str:
        return f'static/ItemPhotos/{self.product_line.name}/{filename}'

    photo = ImageField(upload_to=path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            new_size = (840, 840)
            img.thumbnail(new_size)
            img.save(self.photo.path)

    def __str__(self):
        return f'{self.color} - {self.product_line.name}'


class UserAddress(Model):
    user = ForeignKey(to=User, on_delete=CASCADE)
    address = CharField(max_length=140, blank=True, null=True)
    area_code = CharField(max_length=10, blank=True, null=True)
    unit = CharField(max_length=20, blank=True, null=True)


class UserCart(Model):
    user = ForeignKey(to=User, on_delete=CASCADE)

    def total(self) -> Decimal:
        total_price = Decimal(0)
        for cart_item in self.cartitem_set.all():
            total_price += cart_item.quantity * cart_item.item.price
        return total_price


class CartItem(Model):
    user_cart = ForeignKey(to=UserCart, on_delete=CASCADE)
    item = ForeignKey(to=Item, on_delete=CASCADE)
    quantity = IntegerField(default=1)
    size = CharField(max_length=4)
    per_item_price = DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'{self.item.product_line.name} | {self.item.color} x {self.item.price}'
