# The Coffee Bar ☕

A modern, full-featured artisan coffee shop and online ordering web application built with Django 5, vanilla JavaScript, and modern CSS.

Designed for micro-roasteries, specialty coffee bars, and cafes needing responsive ordering, customizer workflows, order status tracking, and administration.

---

## Highlights & Features

- **Modern Responsive Design**: Custom CSS design system with warm coffee-toned aesthetics, glassmorphism headers, fluid typography, and mobile-friendly drawer navigation.
- **Dynamic Drink Customizer**: Interactive ordering widget with instant client-side price recalculation across cup sizes, dairy/plant milk selections (oat, almond, soy), and sweetness levels.
- **Catalog & Search**: Filter coffee offerings by category, roast profile (Light, Medium, Dark, Specialty), and keyword search.
- **Order Tracking & Live Status**: Multi-step order status stepper (Received &rarr; Brewing &rarr; Quality Check &rarr; Ready for Pickup) with itemized digital receipts.
- **User Authentication & History**: Customer registration, authentication, and a personal order history dashboard.
- **Barista Administration**: Django admin integration with thumbnail image previews, order status tags, inline order items, and category management.
- **Database Seeder**: Built-in management command to populate categories, descriptions, roast metrics, and menu items.
- **Automated Test Suite**: Model and view test coverage with 100% passing tests.

---

## Tech Stack

- **Backend**: Python 3.12+, Django 5 / 6
- **Frontend**: Modern Semantic HTML5, CSS3 Custom Properties (Design System), Vanilla JavaScript (ES6+)
- **Database**: SQLite (Development) / PostgreSQL-ready
- **Media & Images**: Pillow (ImageField support)
- **Environment Management**: python-dotenv

---

## Project Structure

```text
Coffee-Shop/
├── config/                  # Django project configuration & settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── shop/                    # Primary application package
│   ├── management/commands/ # Custom CLI tools (e.g. seed_data)
│   ├── migrations/          # Schema migrations
│   ├── templates/shop/      # Modern templates (home, menu, order, auth)
│   ├── admin.py             # Admin panel customizations
│   ├── forms.py             # Form definitions with validation
│   ├── models.py            # Category, Coffees, Order, OrderItem models
│   ├── tests.py             # Test suite
│   ├── urls.py              # URL routing
│   └── views.py             # View controllers
├── static/                  # Static assets
│   ├── css/styles.css       # Design system and layout styles
│   └── js/main.js           # Interactive UI and live price calculation
├── templates/               # Global templates
│   └── base.html            # Core HTML boilerplate with navigation and footer
├── .env.example             # Sample environment variables
├── .gitignore               # Clean git exclusions
├── manage.py
├── pyproject.toml
└── requirements.txt
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/C0841t-8lu3/Coffee-Shop.git
cd Coffee-Shop
```

### 2. Create and activate a virtual environment

Using `venv`:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Or using `uv`:
```bash
uv venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables (optional)

```bash
cp .env.example .env
```

### 5. Run migrations & seed demo data

```bash
python manage.py migrate
python manage.py seed_data
```

### 6. Create superuser (optional)

```bash
python manage.py createsuperuser
```

*(Note: `python manage.py seed_data` already sets up a demo staff user: username `barista`, password `BaristaPass123!`)*

### 7. Run development server

```bash
python manage.py runserver
```

Open your browser at `http://127.0.0.1:8000/`.

---

## Running Tests

Run the automated test suite with:

```bash
python manage.py test
```

---

## License

This project is licensed under the MIT License.
