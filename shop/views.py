from django.views.generic import TemplateView, ListView
from .models import Coffees
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.shortcuts import redirect


class HomePage(ListView):
    template_name = 'base/home_page.html'
    model = Coffees
    context_object_name = 'coffees'  # Plural for clarity

    def get_queryset(self):
        return Coffees.objects.order_by('name')  # Optional: sort by name


class BuyPage(TemplateView):
    template_name = 'base/buy_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add dynamic context if needed
        return context


class LoginPage(LoginView):
    template_name = 'base/login_page.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


class SignupPage(FormView):
    template_name = 'base/signup_page.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')  # Redirect to home after signup

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')  # Redirect to home for consistency
        return super().get(*args, **kwargs)