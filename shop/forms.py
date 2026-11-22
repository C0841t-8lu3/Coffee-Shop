from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Order, OrderItem, ContactMessage, Coffees


class QuickOrderForm(forms.ModelForm):
    size = forms.ChoiceField(
        choices=OrderItem.SIZE_CHOICES,
        initial='medium',
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'orderSizeSelect'})
    )
    milk = forms.ChoiceField(
        choices=OrderItem.MILK_CHOICES,
        initial='whole',
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'orderMilkSelect'})
    )
    sweetness = forms.ChoiceField(
        choices=[
            ('Unsweetened', 'Unsweetened (0%)'),
            ('Less Sweet', 'Light (50%)'),
            ('Normal', 'Standard Sweetness (100%)'),
            ('Extra Sweet', 'Extra Sweet (125%)'),
        ],
        initial='Normal',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'orderQtyInput'})
    )

    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'customer_phone', 'pickup_type', 'pickup_time', 'notes']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jane Doe', 'required': 'required'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'jane@example.com', 'required': 'required'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 019-2834'}),
            'pickup_type': forms.Select(attrs={'class': 'form-select'}),
            'pickup_time': forms.Select(choices=[
                ('10-15 minutes', 'Express (10 - 15 mins)'),
                ('20-30 minutes', 'Standard (20 - 30 mins)'),
                ('45-60 minutes', 'Later Today (45 - 60 mins)'),
                ('scheduled', 'Custom / In 2 Hours'),
            ], attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Extra hot, oat milk on side, light ice, etc.'}),
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username or Email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '••••••••'
        })


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@domain.com', 'required': 'required'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Catering / Feedback / Inquiries'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'How can our baristas help you today?', 'required': 'required'}),
        }
