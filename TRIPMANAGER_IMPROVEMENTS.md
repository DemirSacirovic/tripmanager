# TripManager - Senior-Level Improvements Documentation

Ovaj dokument detaljno objasnjava sve promene na tripmanager projektu koje demonstriraju senior Python/Django znanje.

---

## 1. Environment Variables za Secrets (Security Best Practice)

**Fajl:** `config/settings.py`

### Kod:
```python
import os

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-dev-only-change-in-production"
)

DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
```

### Zasto je ovo vazno (Interview objasnjenje):

**Problem koji resava:**
- Hardkodovani secreti u kodu su sigurnosni rizik
- Ako commitujete SECRET_KEY u Git, svako ko ima pristup repo-u moze kompromitovati aplikaciju
- Razliciti environment-i (dev/staging/prod) zahtevaju razlicite vrednosti

**Kako funkcionise:**
1. `os.environ.get("KEY", "default")` - cita environment varijablu, ako ne postoji koristi default
2. `DEBUG` koristi `.lower() in ("true", "1", "yes")` - sigurna konverzija stringa u boolean
3. `ALLOWED_HOSTS.split(",")` - pretvara comma-separated string u listu

**Senior-level insight:**
- Default vrednost za SECRET_KEY ima prefiks `django-insecure-` - ovo je Django konvencija koja jasno oznacava da nije za produkciju
- U produkciji biste postavili env vars kroz:
  - Docker/Kubernetes secrets
  - AWS Parameter Store / Secrets Manager
  - HashiCorp Vault

---

## 2. drf-spectacular za API Dokumentaciju (Swagger UI)

**Fajlovi:** `config/settings.py`, `config/urls.py`, `requirements.txt`

### Settings konfiguracija:
```python
INSTALLED_APPS = [
    # ...
    "rest_framework",
    "drf_spectacular",
    "trips",
]

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # ...
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Trip Manager API",
    "DESCRIPTION": "Corporate travel management REST API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
```

### URL konfiguracija:
```python
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # ...
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
```

### Zasto je ovo vazno (Interview objasnjenje):

**Sta je OpenAPI/Swagger:**
- OpenAPI je standard za opisivanje REST API-ja
- Swagger UI je interaktivna dokumentacija gde mozes testirati endpoint-e
- ReDoc je alternativni UI, lepsi za citanje

**Zasto drf-spectacular a ne drf-yasg:**
- drf-spectacular je moderniji, aktivno maintainovan
- Bolja podrska za DRF 3.14+ i Django 4+
- Generise OpenAPI 3.0 (yasg generise 2.0)
- Bolja type inference iz serializer-a

**Kako funkcionise:**
1. `SpectacularAPIView` - generise OpenAPI JSON schema
2. `SpectacularSwaggerView` - renderuje Swagger UI koji koristi tu shemu
3. `url_name="schema"` - povezuje Swagger UI sa schema endpoint-om

**Pristup:**
- Schema JSON: http://localhost:8000/api/schema/
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

---

## 3. DRF Pagination (Scalability)

**Fajl:** `config/settings.py`

### Kod:
```python
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}
```

### Zasto je ovo vazno (Interview objasnjenje):

**Problem bez paginacije:**
- Bez paginacije, `GET /api/trips/` vraca SVE trip-ove
- Sa 10,000 tripova = ogroman JSON response
- Sporo, zauzima memoriju, losa user experience

**Kako funkcionise:**
- `PageNumberPagination` - klasicna paginacija sa page brojevima
- Response format:
```json
{
  "count": 1523,
  "next": "http://localhost:8000/api/trips/?page=2",
  "previous": null,
  "results": [...]
}
```

**Alternativne pagination klase:**
- `LimitOffsetPagination` - `?limit=20&offset=40`
- `CursorPagination` - za infinite scroll, najefikasnija za velike datasete

**Senior-level insight:**
- Za TravelPerk sa hiljadama tripova, pagination je obavezan
- `PAGE_SIZE: 20` je dobar default - nije premalo (previse requestova), nije previse (spori response)

---

## 4. Docker Support

**Fajlovi:** `docker-compose.yml`, `Dockerfile` (ako postoji)

### docker-compose.yml:
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DEBUG=True
      - SECRET_KEY=docker-dev-secret-key-change-in-prod
      - ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
      - DJANGO_SETTINGS_MODULE=config.settings
    command: python manage.py runserver 0.0.0.0:8000
```

### Zasto je ovo vazno (Interview objasnjenje):

**Sta Docker resava:**
- "Works on my machine" problem - svako ima istu environment
- Lako pokretanje projekta - jedan `docker-compose up` umesto instalacije dependencies
- Production-ready - isti kontejner radi u dev i prod

**Kljucni elementi:**
- `volumes: .:/app` - mount-uje kod u kontejner, promene se odmah vide (hot reload)
- `environment` - env vars se prosledjuju u kontejner
- `0.0.0.0:8000` - slusaj na svim interfejsima (potrebno za Docker networking)

**Senior-level insight:**
- Production bi imao odvojene servise (web, db, redis, celery)
- Koristio bi multi-stage build za manji image
- Health checks za production readiness

---

## 5. CI/CD Pipeline (GitHub Actions)

**Fajl:** `.github/workflows/ci.yml`

### Kod:
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run migrations
        run: python manage.py migrate
      - name: Run tests
        run: python manage.py test trips -v 2

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install linting tools
        run: pip install flake8
      - name: Run flake8
        run: flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

### Zasto je ovo vazno (Interview objasnjenje):

**Sta CI radi:**
- Automatski pokrece testove na svakom push/PR
- Hvata bugove pre nego sto dodju u main branch
- Badge u README pokazuje da projekat ima testove

**Matrix testing:**
- `matrix: python-version: ['3.11', '3.12']` - testira na dve verzije
- Osigurava kompatibilnost sa razlicitim Python verzijama

**Lint job:**
- `flake8 --select=E9,F63,F7,F82` - hvata samo kriticne greske
- E9: Syntax errors
- F63: Invalid print syntax
- F7: Syntax errors in type comments
- F82: Undefined names

---

## 6. Testing Dependencies

**Fajl:** `requirements.txt`

```
pytest==8.3.0
pytest-cov==5.0.0
pytest-django==4.9.0
coverage==7.6.0
```

### Zasto je ovo vazno (Interview objasnjenje):

**pytest vs unittest:**
- pytest ima cistiju sintaksu (nema `self.assertEqual`, koristi `assert`)
- Bolje error poruke
- Fixtures za dependency injection
- Parametrized tests

**pytest-django:**
- Integracija sa Django (automatski setup test DB)
- `@pytest.mark.django_db` dekorator
- Fixtures: `client`, `rf` (RequestFactory), `admin_client`

**Coverage:**
- Meri koliki procenat koda je pokriven testovima
- `pytest --cov=trips --cov-report=html` generise HTML report

---

## 7. Service Layer Pattern

**Fajl:** `trips/services.py`

### Kod:
```python
class FlightService:
    """
    Service for searching and booking flights.
    """
    BASE_URL = "https://api.amadeus.com/v2"
    MAX_RETRIES = 3
    INITIAL_BACKOFF = 1  # seconds

    def search_flights(self, origin: str, destination: str, date: str) -> Optional[dict]:
        """Search for available flights."""
        # ...

    def _call_api_with_retry(self, url: str, params: dict, method: str = "GET") -> Optional[dict]:
        """Make API call with exponential backoff retry logic."""
        backoff = self.INITIAL_BACKOFF

        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout on attempt {attempt + 1}")
            except requests.exceptions.HTTPError as e:
                if response.status_code >= 500:
                    logger.warning(f"Server error {response.status_code}")
                else:
                    return None  # Client error - don't retry

            if attempt < self.MAX_RETRIES - 1:
                time.sleep(backoff)
                backoff *= 2  # Exponential backoff

        return None
```

### Zasto je ovo vazno (Interview objasnjenje):

**Service Layer Pattern:**
- Odvaja business logiku od views
- Views su tanki - samo primaju request i vracaju response
- Services sadrze logiku za rad sa external API-jima
- Lakse za testiranje (mozes mock-ovati service)

**Exponential Backoff:**
- Retry logika za unreliable external API-je
- Backoff: 1s -> 2s -> 4s (eksponencijalno)
- Ne retry-uj 4xx greske (client error = tvoja greska)
- Retry samo 5xx i timeout (server error = njihova greska)

**Type Hints:**
```python
def search_flights(self, origin: str, destination: str, date: str) -> Optional[dict]:
```
- `Optional[dict]` znaci "vraca dict ILI None"
- Type hints pomazu IDE-u i dokumentaciji
- Senior-level Python standard od 3.6+

---

## 8. Custom Permissions

**Fajl:** `trips/permissions.py`

### Kod:
```python
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission: read access to any, write access only to owner.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        traveler = getattr(obj, 'traveler', None)
        if traveler is None:
            return False

        return traveler.id == request.user.id
```

### Zasto je ovo vazno (Interview objasnjenje):

**View-level vs Object-level permissions:**
- `has_permission()` - provera pre nego sto se pristupi objektu
- `has_object_permission()` - provera za specifican objekat

**SAFE_METHODS:**
- `GET`, `HEAD`, `OPTIONS` - read-only, ne menjaju podatke
- `POST`, `PUT`, `PATCH`, `DELETE` - write operacije

**Defense in Depth:**
```python
permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
```
- Dva sloja: prvo mora biti ulogovan, pa onda mora biti vlasnik
- Nikad se ne oslanjaj na samo jedan sloj sigurnosti

---

## 9. N+1 Query Prevention

**Fajl:** `trips/views_api.py`

### Kod:
```python
class TripViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        """
        Returns trips with traveler data pre-fetched.
        Uses select_related to prevent N+1 query problem.
        """
        return Trip.objects.select_related('traveler').all()
```

### Zasto je ovo vazno (Interview objasnjenje):

**N+1 Problem:**
```python
# BEZ select_related - N+1 queries
trips = Trip.objects.all()  # 1 query
for trip in trips:
    print(trip.traveler.name)  # N queries (jedan po trip-u)
```

**SA select_related:**
```python
# SA select_related - 1 query sa JOIN
trips = Trip.objects.select_related('traveler').all()
# SQL: SELECT trips.*, travelers.* FROM trips JOIN travelers...
```

**select_related vs prefetch_related:**
- `select_related` - za ForeignKey (one-to-one, many-to-one) - koristi JOIN
- `prefetch_related` - za ManyToMany i reverse FK - koristi 2 upita

---

## 10. Admin Customization

**Fajl:** `trips/admin.py`

### Kod:
```python
@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ["title", "traveler", "destination", "status_badge", "created_at"]
    list_filter = ["status", "start_date", "destination"]
    search_fields = ["title", "destination", "traveler__first_name"]
    list_select_related = ["traveler"]  # N+1 prevention u admin-u
    actions = ["approve_trips", "reject_trips"]

    def status_badge(self, obj):
        """Display status as a colored badge."""
        colors = {"draft": "#6c757d", "pending": "#ffc107", "approved": "#28a745"}
        return format_html(
            '<span style="background-color: {}; padding: 3px 10px;">{}</span>',
            colors.get(obj.status), obj.get_status_display()
        )

    @admin.action(description="Approve selected trips")
    def approve_trips(self, request, queryset):
        updated = queryset.filter(status="pending").update(status="approved")
        self.message_user(request, f"{updated} trip(s) approved.")
```

### Zasto je ovo vazno (Interview objasnjenje):

**Bulk Actions:**
- `@admin.action` - custom akcije u admin-u
- Korisno za approval workflow - odaberi 50 tripova, approve all

**list_select_related:**
- Spreci N+1 u admin listi
- Admin po defaultu ne koristi select_related

**format_html:**
- Siguran nacin za HTML u admin-u (escapa input)
- Nikad nemoj koristiti f-string za HTML - XSS ranjivost

---

## Kako objasniti na intervjuu

### Pitanje: "Objasni arhitekturu ovog projekta"

**Odgovor:**
"Tripmanager je Django REST API za korporativno upravljanje putovanjima. Koristim:
- **DRF ViewSets** za CRUD operacije sa custom actions za workflow (approve/reject)
- **Service layer** za external API integracije sa retry logikom
- **Custom permissions** za owner-based access control
- **select_related** za optimizaciju upita
- **drf-spectacular** za automatsku OpenAPI dokumentaciju

Projekat ima CI pipeline koji testira na Python 3.11 i 3.12, i podrzava Docker deployment."

### Pitanje: "Kako bi skalirao ovu aplikaciju?"

**Odgovor:**
"Za skaliranje bih:
1. Dodao Redis za caching cesto koriscenih upita
2. Koristio Celery za async task-ove (email notifikacije, report generisanje)
3. Prebacio na PostgreSQL sa read replicama
4. Implementirao rate limiting za API
5. Dodao Kubernetes za horizontal scaling"

---

## Checklist za intervju

- [x] Znas objasniti svaki fajl i zasto postoji
- [x] Znas razliku izmedju select_related i prefetch_related
- [x] Znas zasto koristimo environment variables
- [x] Znas objasniti exponential backoff pattern
- [x] Znas razliku izmedju view-level i object-level permissions
- [x] Znas zasto je pagination bitan
- [x] Znas objasniti CI/CD workflow
