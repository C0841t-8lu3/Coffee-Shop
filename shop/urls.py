from django.urls import path
from .views import (
    HomePage,
    MenuPage,
    CoffeeDetailPage,
    BuyPage,
    OrderSuccessView,
    MyOrdersPage,
    ContactView,
    LoginPage,
    SignupPage,
    custom_logout,
)

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('menu/', MenuPage.as_view(), name='menu'),
    path('coffee/<slug:slug>/', CoffeeDetailPage.as_view(), name='coffee_detail'),
    path('order/<int:pk>/', BuyPage.as_view(), name='order'),
    path('order/', BuyPage.as_view(), name='buy'),
    path('order/success/<int:pk>/', OrderSuccessView.as_view(), name='order_success'),
    path('my-orders/', MyOrdersPage.as_view(), name='my_orders'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('login/', LoginPage.as_view(), name='login'),
    path('signup/', SignupPage.as_view(), name='signup'),
    path('logout/', custom_logout, name='logout'),
]
