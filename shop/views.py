from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.db.models import Q

from .models import Coffees, Category, Order, OrderItem, ContactMessage
from .forms import QuickOrderForm, CustomUserCreationForm, CustomLoginForm, ContactForm


class HomePage(TemplateView):
    template_name = 'shop/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_coffees'] = Coffees.objects.filter(is_featured=True, is_available=True)[:6]
        context['all_coffees'] = Coffees.objects.filter(is_available=True)[:8]
        context['categories'] = Category.objects.all()
        context['total_varieties'] = Coffees.objects.filter(is_available=True).count()
        context['contact_form'] = ContactForm()
        return context


class MenuPage(ListView):
    model = Coffees
    template_name = 'shop/menu.html'
    context_object_name = 'coffees'
    paginate_by = 12

    def get_queryset(self):
        qs = Coffees.objects.filter(is_available=True)
        category_slug = self.request.GET.get('category')
        roast = self.request.GET.get('roast')
        query = self.request.GET.get('q')
        sort = self.request.GET.get('sort', 'featured')

        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        if roast:
            qs = qs.filter(roast_level__iexact=roast)
        if query:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(origin__icontains=query)
            )

        if sort == 'price_asc':
            qs = qs.order_by('price')
        elif sort == 'price_desc':
            qs = qs.order_by('-price')
        elif sort == 'rating':
            qs = qs.order_by('-rating')
        elif sort == 'name':
            qs = qs.order_by('name')
        else:
            qs = qs.order_by('-is_featured', 'name')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category', '')
        context['current_roast'] = self.request.GET.get('roast', '')
        context['current_query'] = self.request.GET.get('q', '')
        context['current_sort'] = self.request.GET.get('sort', 'featured')
        return context


class CoffeeDetailPage(DetailView):
    model = Coffees
    template_name = 'shop/coffee_detail.html'
    context_object_name = 'coffee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        coffee = self.get_object()
        context['related_coffees'] = Coffees.objects.filter(
            category=coffee.category,
            is_available=True
        ).exclude(id=coffee.id)[:3]
        context['order_form'] = QuickOrderForm()
        return context


class BuyPage(View):
    """
    Handles ordering directly from product card or customizer page.
    Supports both GET for order configuration and POST for checkout submission.
    """
    def get(self, request, pk=None):
        coffee = None
        if pk:
            coffee = get_object_or_404(Coffees, pk=pk, is_available=True)
        else:
            first_coffee = Coffees.objects.filter(is_available=True).first()
            if first_coffee:
                return redirect('order', pk=first_coffee.pk)

        initial_data = {}
        if request.user.is_authenticated:
            initial_data['customer_name'] = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
            initial_data['customer_email'] = request.user.email

        form = QuickOrderForm(initial=initial_data)
        all_coffees = Coffees.objects.filter(is_available=True)

        return render(request, 'shop/buy_page.html', {
            'coffee': coffee,
            'all_coffees': all_coffees,
            'form': form,
        })

    def post(self, request, pk=None):
        if pk:
            coffee = get_object_or_404(Coffees, pk=pk, is_available=True)
        else:
            coffee_id = request.POST.get('coffee_id')
            coffee = get_object_or_404(Coffees, pk=coffee_id, is_available=True)

        form = QuickOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user

            # Price calculations based on size & milk
            base_price = coffee.price
            size = form.cleaned_data.get('size')
            milk = form.cleaned_data.get('milk')
            qty = form.cleaned_data.get('quantity', 1)

            unit_price = base_price
            if size == 'large':
                unit_price += Decimal('0.80')
            elif size == 'small':
                unit_price = max(Decimal('2.00'), unit_price - Decimal('0.50'))

            if milk in ['oat', 'almond']:
                unit_price += Decimal('0.60')
            elif milk == 'soy':
                unit_price += Decimal('0.50')

            subtotal = unit_price * qty
            order.total_amount = subtotal
            order.status = 'brewing'
            order.save()

            # Create OrderItem
            OrderItem.objects.create(
                order=order,
                coffee=coffee,
                quantity=qty,
                size=size,
                milk=milk,
                sweetness=form.cleaned_data.get('sweetness', 'Normal'),
                unit_price=unit_price,
                subtotal=subtotal
            )

            messages.success(
                request,
                f"🎉 Order #{order.id} placed successfully! Our barista has started crafting your {coffee.name}."
            )
            return redirect('order_success', pk=order.pk)

        all_coffees = Coffees.objects.filter(is_available=True)
        return render(request, 'shop/buy_page.html', {
            'coffee': coffee,
            'all_coffees': all_coffees,
            'form': form,
        })


class OrderSuccessView(DetailView):
    model = Order
    template_name = 'shop/order_success.html'
    context_object_name = 'order'


class MyOrdersPage(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shop/my_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__coffee').order_by('-created_at')


class ContactView(View):
    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "☕ Thank you! Your message has been received. A barista or manager will get back to you shortly.")
        else:
            messages.error(request, "Please check the form fields and submit again.")
        return redirect('home')


class LoginPage(LoginView):
    template_name = 'shop/login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, f"Welcome back, {form.get_user().username}! ☕")
        return super().form_valid(form)


class SignupPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = CustomUserCreationForm()
        return render(request, 'shop/signup.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created successfully! Welcome to Coffee Shop, {user.username}!")
            return redirect('home')
        return render(request, 'shop/signup.html', {'form': form})


def custom_logout(request):
    logout(request)
    messages.info(request, "You have been logged out. Come back soon for fresh coffee! ☕")
    return redirect('home')
