# Expense Tracker

A web application built with Python and Django for tracking personal daily expenses, monitoring monthly budgets, and viewing category breakdowns. Built for **CSC 226: Web Database Applications** (Fall 2026).

## Features

- **User Accounts:** Registration, login, and logout using Django session authentication.
- **Log Expenses:** Add new transactions with amount, category, date, and optional notes.
- **Monthly Spending Dashboard:** View current month spending, transaction counts, and category breakdown.
- **Budget Tracking:** Set a custom monthly budget target with a visual progress bar that alerts you when spending approaches or exceeds your limit.
- **Spending Charts:** Visual category breakdown using Chart.js alongside an accessible breakdown table.
- **Transaction History:** Review all transactions with filtering by category, month, and description search. Includes pagination and CSV export.
- **Safe Deletion:** Delete transactions with confirmation prompts and user ownership verification.

## Tech Stack

- **Backend:** Python 3.14, Django 5.2
- **Database:** SQLite (default for development) or MySQL 8.0 via `pymysql`
- **Frontend:** HTML5, CSS3 with custom properties, Vanilla JavaScript, Chart.js (via CDN)

## Project Structure

```
├── expense_tracker/         # Project configuration
│   ├── settings.py          # Database and application settings
│   ├── urls.py              # Root routing
│   └── wsgi.py              # WSGI entry point
├── tracker/                 # Core tracker application
│   ├── admin.py             # Django admin registration
│   ├── forms.py             # Registration and transaction forms
│   ├── models.py            # Category, UserProfile, and Transaction models
│   ├── queries.py           # Django ORM aggregation and filter queries
│   ├── urls.py              # Application routes
│   ├── views.py             # View controllers and endpoints
│   └── management/          # Custom management commands
│       └── commands/
│           └── seed_categories.py
├── templates/               # HTML templates
│   ├── base.html            # Base layout and navigation
│   ├── registration/        # Login and register pages
│   └── tracker/             # Dashboard, add expense, history pages
├── static/                  # Static assets
│   ├── css/style.css        # Stylesheet and design tokens
│   └── js/ui.js             # Form feedback and UI helpers
├── manage.py
└── requirements.txt
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/SamuelIVX/web-expense-tracker.git
cd web-expense-tracker
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:
```cmd
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables (optional)

By default, the application runs on SQLite with no extra configuration needed.

If you want to use MySQL instead, copy `.env.example` to `.env` and set your credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```env
DB_ENGINE=mysql
DB_NAME=expense_tracker
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 5. Run database migrations

```bash
python manage.py migrate
```

### 6. Seed initial categories

Populate the standard expense categories (Food & Dining, Groceries, Transportation, Utilities, Entertainment, Healthcare, Shopping, Personal Care, Education, Other):

```bash
python manage.py seed_categories
```

### 7. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 8. Run the development server

```bash
python manage.py runserver
```

Open your browser and visit `http://127.0.0.1:8000/`. Register a new account to start logging expenses.
