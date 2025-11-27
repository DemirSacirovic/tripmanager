# Trip Manager

Corporate travel management REST API built with Django and Django REST Framework.

## Features

- **Traveler Management** - Full CRUD for employee travel profiles
- **Trip Workflow** - Draft → Pending → Approved/Rejected status flow
- **Custom Permissions** - Owner-based access control
- **Django Admin** - Customized admin panel with bulk actions
- **Flight Search** - 3rd party API integration with retry logic
- **N+1 Prevention** - Optimized queries with select_related

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.x | Language |
| Django 5.x | Web framework |
| Django REST Framework | API |
| SQLite | Development database |

## Quick Start

```bash
# Clone and setup
git clone https://github.com/DemirSacirovic/tripmanager.git
cd tripmanager

# Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install and run
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

API available at: http://localhost:8000/api/

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/trips/` | GET | List all trips |
| `/api/trips/` | POST | Create new trip |
| `/api/trips/{id}/` | GET/PUT/DELETE | Trip details |
| `/api/trips/{id}/approve/` | POST | Approve pending trip |
| `/api/trips/{id}/reject/` | POST | Reject pending trip |
| `/api/trips/{id}/submit/` | POST | Submit draft for approval |
| `/api/travelers/` | GET/POST | Traveler list/create |

## Testing

```bash
python manage.py test trips
```

## Project Structure

```
tripmanager/
├── config/              # Project settings
├── trips/
│   ├── models.py        # Trip, Traveler models
│   ├── views_api.py     # DRF ViewSets
│   ├── serializers.py   # Request/response validation
│   ├── permissions.py   # Owner-based access control
│   ├── services.py      # External API integration
│   ├── admin.py         # Custom admin configuration
│   └── tests.py         # API tests
└── manage.py
```

## Author

**Demir Sacirovic** - Backend Developer
