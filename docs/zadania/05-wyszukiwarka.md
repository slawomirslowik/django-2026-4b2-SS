# Zadanie 5: Wyszukiwarka pytań

## Cel
Dodaj formularz wyszukiwania pytań po tekście. Użyj metody GET i obiektów Q Django ORM.

---

## Instrukcja krok po kroku

### Krok 1: Dodaj widok wyszukiwania

Otwórz `polls/views.py` i dodaj nowy widok:

```python
from django.db.models import Q

def search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Question.objects.filter(
            Q(question_text__icontains=query),
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')
    return render(request, 'polls/search.html', {
        'results': results,
        'query': query,
    })
```

**Wyjaśnienie:**
- `request.GET.get('q', '')` – pobiera parametr `q` z adresu URL (np. `/polls/search/?q=pogoda`)
- `Q(question_text__icontains=query)` – wyszukuje frazy bez rozróżniania wielkości liter
- `icontains` – odpowiednik SQL `LIKE '%query%'`

---

### Krok 2: Dodaj URL

Otwórz `polls/urls.py` i dodaj:

```python
path('search/', views.search, name='search'),
```

---

### Krok 3: Utwórz szablon `search.html`

Utwórz plik `polls/templates/polls/search.html`:

```html
<h1>Wyszukiwarka pytań</h1>

<form method="get" action="{% url 'polls:search' %}">
    <input type="text" name="q" value="{{ query }}" placeholder="Wpisz szukaną frazę...">
    <button type="submit">Szukaj</button>
</form>

{% if query %}
    <h2>Wyniki dla: "{{ query }}"</h2>
    {% if results %}
        <ul>
        {% for question in results %}
            <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
        {% endfor %}
        </ul>
    {% else %}
        <p>Nie znaleziono pytań pasujących do "{{ query }}".</p>
    {% endif %}
{% endif %}
```

---

### Krok 4: Dodaj link do wyszukiwarki w `index.html`

```html
<a href="{% url 'polls:search' %}">Wyszukaj pytanie</a>
```

---

### Krok 5: Przetestuj

1. Wejdź na `http://127.0.0.1:8000/polls/search/`
2. Wpisz fragment tekstu pytania
3. Sprawdź czy wyniki są poprawne

---

## Rozwiązanie – pełny kod

### `polls/views.py` (nowy widok)

```python
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import render
from .models import Question


def search(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        results = Question.objects.filter(
            Q(question_text__icontains=query),
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')
    return render(request, 'polls/search.html', {
        'results': results,
        'query': query,
    })
```

### `polls/urls.py`

```python
from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('search/', views.search, name='search'),
]
```

### `polls/templates/polls/search.html`

```html
<h1>Wyszukiwarka pytań</h1>

<form method="get" action="{% url 'polls:search' %}">
    <input type="text" name="q" value="{{ query }}" placeholder="Wpisz szukaną frazę...">
    <button type="submit">Szukaj</button>
</form>

{% if query %}
    <h2>Wyniki dla: "{{ query }}"</h2>
    {% if results %}
        <ul>
        {% for question in results %}
            <li>
                <a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a>
                <small>({{ question.pub_date|date:"d.m.Y" }})</small>
            </li>
        {% endfor %}
        </ul>
    {% else %}
        <p>Nie znaleziono pytań pasujących do frazy "{{ query }}".</p>
    {% endif %}
{% endif %}
```
