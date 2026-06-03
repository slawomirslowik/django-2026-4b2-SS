# Zadanie 15: Deployment – wdrożenie projektu na Railway lub Render

## Cel
Wdróż aplikację Django na darmowej platformie chmurowej (Railway lub Render) tak, aby była dostępna publicznie w internecie.

---

## Porównanie platform

| Cecha | Railway | Render |
|---|---|---|
| Darmowy plan | ✅ (5$ credits/mies.) | ✅ (750h/mies.) |
| Baza danych PostgreSQL | ✅ | ✅ |
| Automatyczny deploy z GitHub | ✅ | ✅ |
| Łatwość konfiguracji | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Link | https://railway.app | https://render.com |

---

## Instrukcja – Railway (rekomendowane)

### Krok 1: Przygotuj projekt

Zainstaluj wymagane pakiety:

```
pip install gunicorn whitenoise psycopg2-binary dj-database-url python-decouple
```

Wygeneruj plik `requirements.txt`:

```
pip freeze > requirements.txt
```

---

### Krok 2: Zaktualizuj `settings.py`

```python
import os
from decouple import config
import dj_database_url

SECRET_KEY = config('SECRET_KEY', default='dev-secret-key')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')

# Baza danych – PostgreSQL na produkcji, SQLite lokalnie
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}'
    )
}

# Pliki statyczne (WhiteNoise)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <-- dodaj po SecurityMiddleware
    # ... reszta middleware
]

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

### Krok 3: Utwórz plik `Procfile`

W katalogu głównym projektu utwórz plik `Procfile` (bez rozszerzenia):

```
web: gunicorn mysite.wsgi --chdir myproject
```

---

### Krok 4: Utwórz plik `.env` (lokalnie)

```
SECRET_KEY=twoj-tajny-klucz-django
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

Dodaj `.env` do `.gitignore`:

```
.env
db.sqlite3
__pycache__/
*.pyc
staticfiles/
```

---

### Krok 5: Wypchnij kod na GitHub

```
git add .
git commit -m "Przygotowanie do deployu"
git push origin main
```

---

### Krok 6: Deployuj na Railway

1. Wejdź na https://railway.app i zaloguj się przez GitHub
2. Kliknij **New Project → Deploy from GitHub repo**
3. Wybierz repozytorium `django-2026-4b2-SS`
4. Dodaj bazę danych: **New → Database → Add PostgreSQL**
5. Przejdź do zakładki **Variables** i dodaj zmienne środowiskowe:
   - `SECRET_KEY` – wygeneruj nowy klucz (np. przez https://djecrety.ir/)
   - `DEBUG` – `False`
   - `ALLOWED_HOSTS` – `twoja-domena.up.railway.app`
   - `DATABASE_URL` – skopiuj z zakładki PostgreSQL
6. W zakładce **Settings → Deploy** ustaw **Start Command**: `gunicorn mysite.wsgi --chdir myproject`

---

### Krok 7: Uruchom migracje

W Railway przejdź do zakładki **Shell** i uruchom:

```
cd myproject && python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

---

### Krok 8: Sprawdź

Wejdź na adres wygenerowany przez Railway (np. `https://xxx.up.railway.app/polls/`) i sprawdź działanie aplikacji.

---

## Checklist przed deployem

- [ ] `DEBUG = False` w produkcji
- [ ] `SECRET_KEY` jest tajny i ustawiony przez zmienną środowiskową
- [ ] `ALLOWED_HOSTS` zawiera domenę produkcyjną
- [ ] WhiteNoise obsługuje pliki statyczne
- [ ] `requirements.txt` jest aktualny
- [ ] Baza danych PostgreSQL skonfigurowana
- [ ] Migracje wykonane
- [ ] Superuser utworzony
