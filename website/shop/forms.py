from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import UserAddress


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class AddressForm(ModelForm):
    class Meta:
        model = UserAddress
        fields = '__all__'
        exclude = ['user']
