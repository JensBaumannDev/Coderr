# Coderr Backend

![Python](https://img.shields.io/badge/python-3.14-blue)
![Django](https://img.shields.io/badge/django-6.1-092E20)
![DRF](https://img.shields.io/badge/DRF-3.18-A30000)
![License](https://img.shields.io/badge/license-educational-lightgrey)

A Django REST Framework backend for Coderr, a service marketplace. It handles user authentication, profiles, offers, orders, reviews, and platform statistics, and is built to be consumed by a separate frontend application.

## Frontend

The matching frontend is available in a separate repository:

[Coderr Frontend](https://github.com/Developer-Akademie-Backendkurs/project.Coderr)

## Contents

- [Frontend](#frontend)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Authentication](#authentication)
- [API Overview](#api-overview)
- [Notes for Local Development](#notes-for-local-development)

## Tech Stack

| | |
|---|---|
| Language | Python 3.14 |
| Framework | Django 6.1 |
| API | Django REST Framework 3.18 |
| Auth | Token-based (`rest_framework.authtoken`) |
| Database | SQLite (local development) |
| CORS | django-cors-headers |
| Testing | pytest, pytest-django, pytest-cov |

## Project Structure

```
backend/
├── core/            project settings, root URL config
├── auth_app/        registration, login, and profiles
│   └── api/         serializers, views, urls, permissions
├── offers_app/      offers and offer packages
│   └── api/         serializers, views, urls, permissions
├── orders_app/      orders and order statistics
│   └── api/         serializers, views, urls, permissions
├── reviews_app/     customer reviews
│   └── api/         serializers, views, urls, permissions
├── base_app/        platform statistics
│   └── api/         views and urls
├── manage.py
└── requirements.txt
```

## Getting Started

Quick version, if you just want to get it running:

```bash
git clone https://github.com/JensBaumannDev/Coderr.git
cd Coderr/backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

The API is then available at `http://127.0.0.1:8000/api/`.

### Step by step

**1. Clone the repository**

```bash
git clone https://github.com/JensBaumannDev/Coderr.git
cd Coderr/backend
```

**2. Create and activate a virtual environment**

```bash
python -m venv .venv
```

| OS | Command |
|---|---|
| Windows | `.venv\Scripts\activate` |
| macOS/Linux | `source .venv/bin/activate` |

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Copy the example file and fill in your own secret key:

```bash
cp .env.example .env
```

Generate a key however you like, e.g. with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**5. Apply migrations**

```bash
python manage.py migrate
```

**6. Create a superuser (optional, for the admin site)**

```bash
python manage.py createsuperuser
```

**7. Run the development server**

```bash
python manage.py runserver
```

**8. Start the frontend**

Clone the [Coderr frontend](https://github.com/Developer-Akademie-Backendkurs/project.Coderr) separately and start `index.html` with VS Code's Live Server extension. The backend must be running while using the frontend.

## Authentication

Registration and login return an auth token. Send it with every authenticated request as:

```
Authorization: Token <your-token>
```

## API Overview

**Auth**

| Method | Endpoint |
|---|---|
| POST | `/api/registration/` |
| POST | `/api/login/` |

**Profiles**

| Method | Endpoint |
|---|---|
| GET, PATCH | `/api/profile/<id>/` |
| GET | `/api/profiles/business/` |
| GET | `/api/profiles/customer/` |

**Offers**

| Method | Endpoint |
|---|---|
| GET, POST | `/api/offers/` |
| GET, PATCH, DELETE | `/api/offers/<id>/` |
| GET | `/api/offerdetails/<id>/` |

**Orders**

| Method | Endpoint |
|---|---|
| GET, POST | `/api/orders/` |
| PATCH, DELETE | `/api/orders/<id>/` |
| GET | `/api/order-count/<business_user_id>/` |
| GET | `/api/completed-order-count/<business_user_id>/` |

**Reviews**

| Method | Endpoint |
|---|---|
| GET, POST | `/api/reviews/` |
| PATCH, DELETE | `/api/reviews/<id>/` |

**Statistics**

| Method | Endpoint |
|---|---|
| GET | `/api/base-info/` |

## Notes for Local Development

- The database (`db.sqlite3`) is not tracked in version control. Running the migrations above will create a fresh one.
- `CORS_ALLOWED_ORIGINS` in `core/settings.py` is currently set to `http://127.0.0.1:5500` and `http://localhost:5500`, which match the common ports used by VS Code's Live Server extension when serving the frontend locally. Adjust it if your frontend runs elsewhere.
- This backend is meant to be used together with the [Coderr frontend](https://github.com/Developer-Akademie-Backendkurs/project.Coderr), which lives in its own repository and is not part of this one.
- Django admin is available at `/admin/` once a superuser has been created.
