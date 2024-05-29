from django.urls import path

from . import views


app_name = 'payments'
urlpatterns = [
    path('cart', views.ShoppingCartView.as_view(), name='cart'),
    path('checkout', views.CheckoutView.as_view(), name='checkout'),
]
