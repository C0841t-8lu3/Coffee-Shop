from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shop.models import Category, Coffees, Order, OrderItem, ContactMessage


class CoffeeShopModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Espresso Classics",
            icon="☕"
        )
        self.coffee = Coffees.objects.create(
            category=self.category,
            name="Spanish Cortado",
            description="Silky textured whole milk with espresso.",
            price=Decimal("4.25"),
            roast_level="Medium",
            rating=Decimal("4.9"),
            origin="Colombia"
        )

    def test_category_creation_and_slug(self):
        self.assertEqual(self.category.slug, "espresso-classics")
        self.assertEqual(str(self.category), "Espresso Classics")

    def test_coffee_slug_auto_generation(self):
        self.assertEqual(self.coffee.slug, "spanish-cortado")
        self.assertIn("Spanish Cortado", str(self.coffee))

    def test_coffee_display_image_fallback(self):
        self.assertTrue(self.coffee.display_image.startswith("http"))

    def test_order_creation_and_item(self):
        order = Order.objects.create(
            customer_name="John Doe",
            customer_email="john@example.com",
            total_amount=Decimal("4.25"),
            status="brewing"
        )
        item = OrderItem.objects.create(
            order=order,
            coffee=self.coffee,
            quantity=1,
            size="medium",
            milk="whole",
            unit_price=Decimal("4.25"),
            subtotal=Decimal("4.25")
        )
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(item.coffee.name, "Spanish Cortado")
        self.assertIn("John Doe", str(order))


class CoffeeShopViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Cold Brews", icon="🧊")
        self.coffee = Coffees.objects.create(
            category=self.category,
            name="Nitro Cold Brew",
            description="Slow-steeped nitrogen infused coffee.",
            price=Decimal("5.50"),
            roast_level="Dark",
            is_featured=True,
            is_available=True
        )

    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Coffee Bar")
        self.assertContains(response, "Nitro Cold Brew")

    def test_menu_page_filtering(self):
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nitro Cold Brew")

        # Test search query
        response_search = self.client.get(reverse('menu'), {'q': 'Nitro'})
        self.assertEqual(response_search.status_code, 200)
        self.assertContains(response_search, "Nitro Cold Brew")

        # Test no match
        response_empty = self.client.get(reverse('menu'), {'q': 'NonExistentBeverage'})
        self.assertEqual(response_empty.status_code, 200)
        self.assertContains(response_empty, "No coffees match your filter")

    def test_coffee_detail_view(self):
        url = reverse('coffee_detail', kwargs={'slug': self.coffee.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nitro Cold Brew")
        self.assertContains(response, "$5.50")

    def test_buy_page_get(self):
        url = reverse('order', kwargs={'pk': self.coffee.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Customize & Place Your Order")

    def test_buy_page_post_creates_order(self):
        url = reverse('order', kwargs={'pk': self.coffee.pk})
        post_data = {
            'customer_name': 'Alice Smith',
            'customer_email': 'alice@example.com',
            'customer_phone': '555-0192',
            'pickup_type': 'in_store',
            'pickup_time': '10-15 minutes',
            'notes': 'Extra napkin please',
            'size': 'large',
            'milk': 'oat',
            'sweetness': 'Normal',
            'quantity': 2,
        }
        response = self.client.post(url, post_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check order was created
        order = Order.objects.filter(customer_email='alice@example.com').first()
        self.assertIsNotNone(order)
        self.assertEqual(order.items.count(), 1)
        # Large (+$0.80) + Oat (+$0.60) + Base ($5.50) = $6.90 * 2 = $13.80
        self.assertEqual(order.total_amount, Decimal('13.80'))

    def test_contact_form_submission(self):
        url = reverse('contact')
        data = {
            'name': 'Bob Visitor',
            'email': 'bob@test.com',
            'subject': 'Inquiry about coffee beans',
            'message': 'Do you sell 1kg bags of whole beans?'
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ContactMessage.objects.filter(email='bob@test.com').exists())

    def test_signup_and_login_views(self):
        signup_url = reverse('signup')
        get_res = self.client.get(signup_url)
        self.assertEqual(get_res.status_code, 200)

        login_url = reverse('login')
        login_res = self.client.get(login_url)
        self.assertEqual(login_res.status_code, 200)
