from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('item/<str:pk>', views.itemPage, name='item-page'),
    # authentication
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.register, name='register'),
    # user
    path('profile/<str:pk>', views.profile, name='profile'),
    path('test-user', views.testUser, name='test-user'),
    # cart
    path('cart/', views.viewCart, name='view-cart'),
    path('add/', views.addToCart, name='add-to-cart'),
    path('delete<str:cart_item_id>', views.removeCartItem, name='delete'),
    path('update-cart/<str:cart_item_id>', views.updateCartItem, name='update-cart'),
]
