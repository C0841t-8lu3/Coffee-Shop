from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import LoginPage, SignupPage, BuyPage, HomePage

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('order/<int:pk>/', BuyPage.as_view(), name='order'),
    path('login/', LoginPage.as_view(), name='login'),
    path('signup/', SignupPage.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
