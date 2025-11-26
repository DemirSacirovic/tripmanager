  ```markdown
  # Trip Manager

  Corporate travel management system built with Django and Django REST
  Framework.

  ## Features

  - Traveler management (CRUD operations)
  - Trip management with approval workflow
  - Flight search integration (3rd party API ready)
  - Custom permissions (owner-based access control)
  - RESTful API with browsable interface

  ## Tech Stack

  - Python 3.x
  - Django 5.x
  - Django REST Framework
  - SQLite (development)

  ## Installation

  1. Clone the repository
  2. Create virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate
  3. Install dependencies:
  pip install django djangorestframework requests
  4. Run migrations:
  python manage.py migrate
  5. Create superuser:
  python manage.py createsuperuser
  6. Run server:
  python manage.py runserver

  API Endpoints

  | Endpoint                 | Method | Description        |
  |--------------------------|--------|--------------------|
  | /api/trips/              | GET    | List all trips     |
  | /api/trips/              | POST   | Create new trip    |
  | /api/trips/{id}/         | GET    | Get trip details   |
  | /api/trips/{id}/approve/ | POST   | Approve trip       |
  | /api/trips/{id}/reject/  | POST   | Reject trip        |
  | /api/travelers/          | GET    | List all travelers |

  Running Tests

  python manage.py test

  Project Structure

  tripmanager/
  ├── config/          # Django project settings
  ├── trips/           # Main application
  │   ├── models.py    # Data models (Trip, Traveler)
  │   ├── views_api.py # DRF ViewSets
  │   ├── serializers.py
  │   ├── permissions.py
  │   └── services.py  # External API integration
  └── manage.py

  ---
