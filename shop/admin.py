from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Coffees, Order, OrderItem, ContactMessage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'order', 'coffees_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('order', 'name')

    def coffees_count(self, obj):
        return obj.coffees.count()
    coffees_count.short_description = "Coffees"


@admin.register(Coffees)
class CoffeesAdmin(admin.ModelAdmin):
    list_display = ('preview_thumb', 'name', 'category', 'price', 'roast_level', 'rating', 'is_featured', 'is_available')
    list_filter = ('category', 'roast_level', 'caffeine_level', 'is_featured', 'is_available')
    search_fields = ('name', 'description', 'origin')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'is_featured', 'is_available')
    ordering = ('-is_featured', 'name')

    def preview_thumb(self, obj):
        url = obj.display_image
        return format_html(
            '<img src="{}" style="width: 44px; height: 44px; object-fit: cover; border-radius: 8px; border: 1px solid #ddd;" />',
            url
        )
    preview_thumb.short_description = "Preview"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_email', 'pickup_type', 'total_amount', 'status_badge', 'created_at')
    list_filter = ('status', 'pickup_type', 'created_at')
    search_fields = ('id', 'customer_name', 'customer_email', 'customer_phone')
    inlines = [OrderItemInline]
    readonly_fields = ('total_amount', 'created_at', 'updated_at')
    list_editable = ()

    def status_badge(self, obj):
        colors = {
            'received': '#0284c7',
            'brewing': '#d97706',
            'ready': '#16a34a',
            'completed': '#4b5563',
            'cancelled': '#dc2626',
        }
        color = colors.get(obj.status, '#374151')
        return format_html(
            '<span style="background:{}; color:#fff; padding:4px 10px; border-radius:12px; font-weight:600; font-size:12px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = "Status"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
