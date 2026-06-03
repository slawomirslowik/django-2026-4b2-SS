# Zadanie: Dodanie aplikacji polls i stworzenie pierwszych widoków (Django Tutorial cz. 1)

Na podstawie oficjalnego tutoriala Django: [https://docs.djangoproject.com/en/6.0/intro/tutorial01/](https://docs.djangoproject.com/en/6.0/intro/tutorial01/)

## Krok 1: Utworzenie aplikacji polls

W terminalu, będąc w katalogu głównym projektu, uruchom:

```
py manage.py startapp polls
```

Po wykonaniu tej komendy pojawi się folder `polls` z plikami aplikacji.

---

## Krok 2: Dodanie aplikacji polls do INSTALLED_APPS

Otwórz plik `mysite/settings.py` i dodaj `'polls'` do listy `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...existing code...
    'polls.apps.PollsConfig',
]
```

---

## Krok 3: Utworzenie pierwszego widoku

W pliku `polls/views.py` dodaj funkcję widoku:

```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

---

## Krok 4: Utworzenie pliku urls.py w aplikacji polls

W folderze `polls` utwórz plik `urls.py` i dodaj:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

---

## Krok 5: Dodanie trasy do aplikacji polls w głównym pliku urls.py

Otwórz plik `mysite/urls.py` i dodaj import oraz trasę:

```python
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    ...existing code...
]
```

---

## Krok 6: Uruchomienie serwera i test

W terminalu uruchom serwer:

```
py manage.py runserver
```

Przejdź do przeglądarki i wpisz adres:

```
http://127.0.0.1:8000/polls/
```

Powinieneś zobaczyć komunikat: `Hello, world. You're at the polls index.`

---

**Zadanie wykonane zgodnie z tutorialem Django cz. 1.**