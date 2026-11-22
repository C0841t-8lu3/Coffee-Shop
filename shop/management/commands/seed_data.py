from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Category, Coffees


class Command(BaseCommand):
    help = 'Seeds database with realistic artisan coffee catalog, categories, and demo data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting coffee catalog seed...'))

        # Create or get superuser/admin if needed
        demo_user, _ = User.objects.get_or_create(
            username='barista',
            defaults={
                'email': 'barista@coffeeshop.local',
                'is_staff': True,
            }
        )
        if not demo_user.has_usable_password():
            demo_user.set_password('BaristaPass123!')
            demo_user.save()

        # Categories
        categories_data = [
            {'name': 'Espresso & Classics', 'slug': 'espresso-classics', 'icon': '☕', 'order': 1},
            {'name': 'Iced & Cold Brews', 'slug': 'iced-cold-brews', 'icon': '🧊', 'order': 2},
            {'name': 'Artisan Lattes', 'slug': 'artisan-lattes', 'icon': '✨', 'order': 3},
            {'name': 'Single Origin Drip', 'slug': 'single-origin-drip', 'icon': '🌱', 'order': 4},
            {'name': 'Bakery & Pastries', 'slug': 'bakery-pastries', 'icon': '🥐', 'order': 5},
        ]

        cat_objs = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            cat_objs[cat.slug] = cat
            if created:
                self.stdout.write(f"  Created category: {cat.name}")

        # Items
        coffees_data = [
            {
                'category': cat_objs['espresso-classics'],
                'name': 'Velvet Spanish Cortado',
                'short_description': 'Equal parts silky steamed milk and bold double-shot espresso.',
                'description': 'A Spanish coffee house staple. Perfectly balanced with equal parts espresso and silky textured whole milk to cut the acidity while accentuating sweet caramel and roasted hazelnut undertones.',
                'price': 4.25,
                'rating': 4.9,
                'reviews_count': 84,
                'roast_level': 'Medium',
                'caffeine_level': 'Regular',
                'origin': 'Antioquia, Colombia',
                'calories': 80,
                'image_url': 'https://images.unsplash.com/photo-1534778101976-62847782c213?auto=format&fit=crop&w=700&q=80',
                'is_featured': True,
                'is_available': True,
            },
            {
                'category': cat_objs['espresso-classics'],
                'name': 'Double Ristretto Espresso',
                'short_description': 'Intense, short-pulled shots with a thick hazelnut crema.',
                'description': 'Short-extracted double shot capturing purely the sweetest aromatic compounds and essential coffee oils, avoiding harsher bitter tannins. Finished with a dense, velvety tiger-striped crema.',
                'price': 3.50,
                'rating': 4.8,
                'reviews_count': 62,
                'roast_level': 'Dark',
                'caffeine_level': 'High',
                'origin': 'Guatemala & Brazil Blend',
                'calories': 5,
                'image_url': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=700&q=80',
                'is_featured': False,
                'is_available': True,
            },
            {
                'category': cat_objs['iced-cold-brews'],
                'name': 'Salted Caramel Nitro Cold Brew',
                'short_description': 'Slow-steeped 20 hours, infused with nitrogen & house caramel.',
                'description': 'Steeped cold for 20 hours in small batches, charged with micro-nitrogen bubbles for a Guinness-like cascading texture, and topped with house-made smoked salted caramel cold foam.',
                'price': 5.75,
                'rating': 5.0,
                'reviews_count': 148,
                'roast_level': 'Medium',
                'caffeine_level': 'High',
                'origin': 'Sumatra Lintong',
                'calories': 140,
                'image_url': 'https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?auto=format&fit=crop&w=700&q=80',
                'is_featured': True,
                'is_available': True,
            },
            {
                'category': cat_objs['iced-cold-brews'],
                'name': 'Artisan Brown Sugar Shaken Espresso',
                'short_description': 'Blonde espresso, organic brown sugar, and toasted oat milk.',
                'description': 'Fresh espresso shots vigorously hand-shaken with ice, raw demerara sugar, and a hint of cinnamon bark, finished with a pour of chilled oat milk for an airy froth and caramelized flavor.',
                'price': 5.25,
                'rating': 4.9,
                'reviews_count': 112,
                'roast_level': 'Light',
                'caffeine_level': 'High',
                'origin': 'Ethiopia Sidamo',
                'calories': 110,
                'image_url': 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=700&q=80',
                'is_featured': True,
                'is_available': True,
            },
            {
                'category': cat_objs['artisan-lattes'],
                'name': 'Honey Lavender Oat Latte',
                'short_description': 'Wildflower honey, French culinary lavender & creamy oat milk.',
                'description': 'Delicate French lavender flowers infused into local wildflower honey, paired with a mellow double espresso and steamed oat milk. Mild, floral, and soothing with velvety mouthfeel.',
                'price': 5.95,
                'rating': 4.9,
                'reviews_count': 97,
                'roast_level': 'Medium',
                'caffeine_level': 'Regular',
                'origin': 'Costa Rica Tarrazu',
                'calories': 160,
                'image_url': 'https://images.unsplash.com/photo-1577968897966-3d4325b36b61?auto=format&fit=crop&w=700&q=80',
                'is_featured': True,
                'is_available': True,
            },
            {
                'category': cat_objs['artisan-lattes'],
                'name': 'Madagascar Vanilla Flat White',
                'short_description': 'Pure bourbon vanilla bean with micro-textured whole milk.',
                'description': 'Originating from Wellington and Melbourne coffee traditions, our Flat White uses real Madagascar bourbon vanilla bean caviar infused in whole milk, folded over double ristretto espresso.',
                'price': 5.15,
                'rating': 4.8,
                'reviews_count': 79,
                'roast_level': 'Medium',
                'caffeine_level': 'Regular',
                'origin': 'Honduras Marcala',
                'calories': 150,
                'image_url': 'https://images.unsplash.com/photo-1541167760496-1628856ab772?auto=format&fit=crop&w=700&q=80',
                'is_featured': False,
                'is_available': True,
            },
            {
                'category': cat_objs['artisan-lattes'],
                'name': 'Ceremonial Matcha Cloud Latte',
                'short_description': 'First-harvest Uji matcha whisked with warm vanilla oat milk.',
                'description': 'Stone-ground first harvest organic green tea leaves directly from Uji, Kyoto. Whisked traditionally with a bamboo chasen and topped with silky oat milk cloud foam.',
                'price': 5.50,
                'rating': 4.9,
                'reviews_count': 88,
                'roast_level': 'Specialty',
                'caffeine_level': 'Regular',
                'origin': 'Uji, Kyoto, Japan',
                'calories': 130,
                'image_url': 'https://images.unsplash.com/photo-1536256263959-770b48d82b0a?auto=format&fit=crop&w=700&q=80',
                'is_featured': False,
                'is_available': True,
            },
            {
                'category': cat_objs['single-origin-drip'],
                'name': 'Ethiopian Yirgacheffe Pour Over',
                'short_description': 'Handcrafted V60 pour over with bergamot, jasmine & lemon notes.',
                'description': 'Grown at 2,000 meters altitude and naturally washed. Features vibrant acidity reminiscent of Meyer lemon, aromatic jasmine blossom aroma, and a clean tea-like finish.',
                'price': 4.85,
                'rating': 4.9,
                'reviews_count': 130,
                'roast_level': 'Light',
                'caffeine_level': 'Regular',
                'origin': 'Yirgacheffe, Ethiopia',
                'calories': 5,
                'image_url': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=700&q=80',
                'is_featured': True,
                'is_available': True,
            },
            {
                'category': cat_objs['single-origin-drip'],
                'name': 'French Press Dark Sumatra',
                'short_description': 'Full-bodied, earthy immersion brew with dark cocoa & cedar.',
                'description': 'Coarsely ground wet-hulled Indonesian beans immersed in boiling water for four minutes, pressing out a heavy, syrup-like body with dark chocolate, pipe tobacco, and forest floor tones.',
                'price': 4.50,
                'rating': 4.7,
                'reviews_count': 54,
                'roast_level': 'Dark',
                'caffeine_level': 'High',
                'origin': 'Aceh, Northern Sumatra',
                'calories': 5,
                'image_url': 'https://images.unsplash.com/photo-1518832553480-cd0e625ed3e6?auto=format&fit=crop&w=700&q=80',
                'is_featured': False,
                'is_available': True,
            },
            {
                'category': cat_objs['bakery-pastries'],
                'name': 'Classic French Butter Croissant',
                'short_description': '48-hour laminated French pastry with flaky golden crust.',
                'description': 'Baked fresh every sunrise using imported Normandy butter. Flaky golden crust that shatters on first bite with a honeycomb aerated interior.',
                'price': 3.95,
                'rating': 4.9,
                'reviews_count': 165,
                'roast_level': 'Specialty',
                'caffeine_level': 'Decaf',
                'origin': 'House Patisserie',
                'calories': 260,
                'image_url': 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=700&q=80',
                'is_featured': True,
                'is_available': True,
            },
            {
                'category': cat_objs['bakery-pastries'],
                'name': 'Pistachio Cardamom Brioche',
                'short_description': 'Rich brioche swirl with roasted pistachio cream & spice.',
                'description': 'Tender brioche dough swirled with freshly roasted Iranian pistachio butter, sweet green cardamom seeds, and topped with chopped pistachios and powdered sugar glaze.',
                'price': 4.75,
                'rating': 4.8,
                'reviews_count': 72,
                'roast_level': 'Specialty',
                'caffeine_level': 'Decaf',
                'origin': 'House Patisserie',
                'calories': 320,
                'image_url': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=700&q=80',
                'is_featured': False,
                'is_available': True,
            },
        ]

        created_count = 0
        for data in coffees_data:
            coffee, created = Coffees.objects.update_or_create(
                name=data['name'],
                defaults={**data, 'user': demo_user}
            )
            if created:
                created_count += 1
                self.stdout.write(f"  + Added coffee: {coffee.name}")

        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded database! Added {len(categories_data)} categories and {created_count} coffee items."
        ))
