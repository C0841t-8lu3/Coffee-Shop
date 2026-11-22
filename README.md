<div align="center">

# ☕ The Coffee Bar

**A modern, full-stack artisan coffee shop & online ordering platform built with Django.**

[![Django](https://img.shields.io/badge/Django-5.2%2B-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-amber?style=for-the-badge)](LICENSE)
[![Tests: Passing](https://img.shields.io/badge/Tests-Passing-success?style=for-the-badge)](shop/tests.py)

[Features](#-features) • [Quickstart](#-quickstart) • [Project Structure](#-project-structure) • [Running Tests](#-running-tests) • [License](#-license)

</div>

---

## 📖 Overview

**The Coffee Bar** is a clean, responsive web application designed for specialty coffee roasteries and neighborhood cafes. It provides a complete workflow from browsing single-origin roasts to real-time custom drink orders, automated receipt generation, and a barista back-office portal.

---

## ✨ Features

- **Responsive Artisan Design**: Handcrafted CSS design system inspired by specialty coffee culture, complete with glassmorphism navigation, warm typography, and smooth transitions.
- **Dynamic Drink Customizer**: Live client-side price calculator factoring in cup sizing (8oz, 12oz, 16oz), plant milk upgrades (oat, almond, soy), and sweetness adjustments.
- **Roast & Category Filtering**: Browse single-origin coffees and pastries filtered by roast profile (Light, Medium, Dark, Specialty) or keyword search.
- **Live Order Tracker**: Visual order progress stepper (*Received &rarr; Brewing &rarr; Quality Check &rarr; Ready for Pickup*) with itemized digital receipts.
- **User Accounts & Order History**: Authentication flow for guests to create accounts, sign in, and view past orders.
- **Barista Admin Dashboard**: Django admin integration with drink thumbnail previews, order status badges, and inline item tracking.
- **Instant Demo Seeder**: Includes `python manage.py seed_data` to automatically populate realistic artisan coffee data and categories.
- **Fully Tested**: Comprehensive unit test suite covering models, ordering calculations, forms, and views.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12+, Django 5 / 6
- **Frontend**: Semantic HTML5, CSS3 Custom Properties, Vanilla JavaScript (ES6+)
- **Database**: SQLite (local development) / PostgreSQL-compatible
- **Image Processing**: Pillow
- **Configuration**: python-dotenv

---

## 🚀 Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/C0841t-8lu3/Coffee-Shop.git
cd Coffee-Shop
```

### 2. Set up a virtual environment

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

### 4. Setup environment variables (optional)

```bash
cp .env.example .env
```

### 5. Run migrations & seed data

```bash
python manage.py migrate
python manage.py seed_data
```

*(This seeds categories and creates a demo staff account: `barista` / `BaristaPass123!`)*

### 6. Start the development server

```bash
python manage.py runserver
```

Visit [`http://127.0.0.1:8000`](http://127.0.0.1:8000) in your browser.

---

## 📁 Project Structure

```text
Coffee-Shop/
├── config/                  # Django project configuration & settings
│   ├── settings.py          # Environment-aware settings
│   ├── urls.py              # Root routing & static file serving
│   └── wsgi.py
├── shop/                    # Core shop application
│   ├── management/commands/ # Custom CLI commands (seed_data)
│   ├── migrations/          # Database migrations
│   ├── templates/shop/      # Shop views (home, menu, customizer, orders)
│   ├── admin.py             # Admin panel customizations
│   ├── forms.py             # Order & contact forms with validation
│   ├── models.py            # Coffees, Category, Order, OrderItem
│   ├── tests.py             # 11 unit tests covering all features
│   ├── urls.py              # Shop route definitions
│   └── views.py             # Class-based and function views
├── static/                  # Static assets
│   ├── css/styles.css       # Complete CSS design system
│   └── js/main.js           # Client-side price math and animations
├── templates/               # Global layout templates
│   └── base.html            # Shared base template
├── .env.example
├── .gitignore
├── manage.py
├── pyproject.toml
└── requirements.txt
```

---

## 🧪 Running Tests

Run the test suite with Django's test runner:

```bash
python manage.py test
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.
