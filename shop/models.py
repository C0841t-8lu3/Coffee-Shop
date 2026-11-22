from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    icon = models.CharField(max_length=50, default='coffee', help_text="Icon identifier (e.g. coffee, flame, cup, sparkle)")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Coffees(models.Model):
    ROAST_CHOICES = [
        ('Light', 'Light Roast'),
        ('Medium', 'Medium Roast'),
        ('Dark', 'Dark Roast'),
        ('Specialty', 'Specialty Brew'),
    ]

    CAFFEINE_CHOICES = [
        ('Regular', 'Regular'),
        ('High', 'High Caffeine'),
        ('Decaf', 'Decaffeinated'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='coffees'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='coffees'
    )
    name = models.CharField(max_length=250, null=False, blank=False)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField(null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=4.50)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.9)
    reviews_count = models.PositiveIntegerField(default=42)
    roast_level = models.CharField(max_length=20, choices=ROAST_CHOICES, default='Medium')
    caffeine_level = models.CharField(max_length=20, choices=CAFFEINE_CHOICES, default='Regular')
    origin = models.CharField(max_length=150, default='Artisan Blend')
    calories = models.PositiveIntegerField(default=120)
    picture = models.ImageField(upload_to='pictures/coffees', null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Coffee"
        verbose_name_plural = "Coffees"
        ordering = ['-is_featured', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Coffees.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def display_image(self):
        if self.picture:
            try:
                return self.picture.url
            except (ValueError, AttributeError):
                pass
        if self.image_url:
            return self.image_url
        return "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=700&q=80"

    def __str__(self):
        return f"{self.name} (${self.price})"


# Alias for clean idiomatic usage
Coffee = Coffees


class Order(models.Model):
    STATUS_CHOICES = [
        ('received', 'Order Received'),
        ('brewing', 'Brewing & Crafting'),
        ('ready', 'Ready for Pickup'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PICKUP_CHOICES = [
        ('in_store', 'In-Store Pickup'),
        ('curbside', 'Curbside Express'),
        ('dine_in', 'Dine-In Table Service'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=30, blank=True)
    pickup_type = models.CharField(max_length=20, choices=PICKUP_CHOICES, default='in_store')
    pickup_time = models.CharField(max_length=50, default='15-20 minutes')
    notes = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name} (${self.total_amount})"


class OrderItem(models.Model):
    SIZE_CHOICES = [
        ('small', 'Small (8oz)'),
        ('medium', 'Regular (12oz)'),
        ('large', 'Large (16oz) +$0.80'),
    ]

    MILK_CHOICES = [
        ('whole', 'Whole Milk'),
        ('oat', 'Oat Milk (+$0.60)'),
        ('almond', 'Almond Milk (+$0.60)'),
        ('soy', 'Soy Milk (+$0.50)'),
        ('none', 'No Milk / Black'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    coffee = models.ForeignKey(Coffees, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, default='medium')
    milk = models.CharField(max_length=20, choices=MILK_CHOICES, default='whole')
    sweetness = models.CharField(max_length=30, default='Normal')
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.coffee.name} ({self.get_size_display()})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} <{self.email}>"
