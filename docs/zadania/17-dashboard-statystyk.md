# Zadanie 17: Dashboard statystyk

## Cel
Stwórz osobną stronę z podsumowaniem wszystkich ankiet: łączna liczba głosów, top pytania, wykres aktywności.

---

## Instrukcja krok po kroku

### Krok 1: Dodaj widok dashboard

Otwórz `polls/views.py` i dodaj:

```python
from django.db.models import Sum, Count
from django.utils import timezone
import datetime


def dashboard(request):
    # Łączna liczba pytań i głosów
    total_questions = Question.objects.filter(pub_date__lte=timezone.now()).count()
    total_votes = Choice.objects.aggregate(total=Sum('votes'))['total'] or 0

    # Top 5 pytań z największą liczbą głosów
    top_questions = Question.objects.filter(
        pub_date__lte=timezone.now()
    ).annotate(
        total_votes=Sum('choice__votes')
    ).order_by('-total_votes')[:5]

    # Ostatnio dodane pytania (ostatnie 7 dni)
    week_ago = timezone.now() - datetime.timedelta(days=7)
    recent_questions = Question.objects.filter(
        pub_date__gte=week_ago,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')

    # Pytania bez głosów
    no_votes_questions = Question.objects.filter(
        pub_date__lte=timezone.now()
    ).annotate(
        total_votes=Sum('choice__votes')
    ).filter(total_votes__isnull=True)

    return render(request, 'polls/dashboard.html', {
        'total_questions': total_questions,
        'total_votes': total_votes,
        'top_questions': top_questions,
        'recent_questions': recent_questions,
        'no_votes_count': no_votes_questions.count(),
    })
```

---

### Krok 2: Dodaj URL

W `polls/urls.py`:

```python
path('dashboard/', views.dashboard, name='dashboard'),
```

---

### Krok 3: Utwórz szablon `dashboard.html`

```html
{% extends 'polls/base.html' %}

{% block title %}Dashboard{% endblock %}

{% block content %}
<h1 class="mb-4">📊 Dashboard statystyk</h1>

<!-- Karty z liczbami -->
<div class="row mb-4">
    <div class="col-md-4">
        <div class="card text-white bg-primary">
            <div class="card-body text-center">
                <h2>{{ total_questions }}</h2>
                <p>Aktywnych ankiet</p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card text-white bg-success">
            <div class="card-body text-center">
                <h2>{{ total_votes }}</h2>
                <p>Łącznie oddanych głosów</p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card text-white bg-warning">
            <div class="card-body text-center">
                <h2>{{ no_votes_count }}</h2>
                <p>Ankiet bez głosów</p>
            </div>
        </div>
    </div>
</div>

<!-- Top 5 pytań -->
<h2 class="mt-4">🏆 Top 5 ankiet</h2>
<table class="table table-striped">
    <thead>
        <tr><th>#</th><th>Pytanie</th><th>Głosy</th><th></th></tr>
    </thead>
    <tbody>
    {% for q in top_questions %}
        <tr>
            <td>{{ forloop.counter }}</td>
            <td>{{ q.question_text }}</td>
            <td><strong>{{ q.total_votes|default:"0" }}</strong></td>
            <td><a href="{% url 'polls:results' q.id %}" class="btn btn-sm btn-outline-primary">Wyniki</a></td>
        </tr>
    {% empty %}
        <tr><td colspan="4">Brak danych.</td></tr>
    {% endfor %}
    </tbody>
</table>

<!-- Ostatnio dodane -->
<h2 class="mt-4">🕐 Dodane w ostatnim tygodniu</h2>
{% if recent_questions %}
    <ul class="list-group">
    {% for q in recent_questions %}
        <li class="list-group-item d-flex justify-content-between">
            <a href="{% url 'polls:detail' q.id %}">{{ q.question_text }}</a>
            <small class="text-muted">{{ q.pub_date|date:"d.m.Y H:i" }}</small>
        </li>
    {% endfor %}
    </ul>
{% else %}
    <p class="text-muted">Brak nowych ankiet w ostatnim tygodniu.</p>
{% endif %}

{% endblock %}
```

---

### Krok 4: Dodaj link do dashboardu w nawigacji

W `base.html` (lub `index.html`) dodaj:

```html
<a href="{% url 'polls:dashboard' %}">Dashboard</a>
```

---

### Krok 5: Przetestuj

Wejdź na `http://127.0.0.1:8000/polls/dashboard/` i sprawdź wyświetlanie statystyk.

---

## Rozwiązanie – pełny kod widoku

```python
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone
import datetime
from .models import Question, Choice


def dashboard(request):
    now = timezone.now()
    week_ago = now - datetime.timedelta(days=7)

    total_questions = Question.objects.filter(pub_date__lte=now).count()
    total_votes = Choice.objects.aggregate(total=Sum('votes'))['total'] or 0

    top_questions = (
        Question.objects
        .filter(pub_date__lte=now)
        .annotate(total_votes=Sum('choice__votes'))
        .order_by('-total_votes')[:5]
    )

    recent_questions = (
        Question.objects
        .filter(pub_date__gte=week_ago, pub_date__lte=now)
        .order_by('-pub_date')
    )

    no_votes_count = (
        Question.objects
        .filter(pub_date__lte=now)
        .annotate(total_votes=Sum('choice__votes'))
        .filter(total_votes__isnull=True)
        .count()
    )

    return render(request, 'polls/dashboard.html', {
        'total_questions': total_questions,
        'total_votes': total_votes,
        'top_questions': top_questions,
        'recent_questions': recent_questions,
        'no_votes_count': no_votes_count,
    })
```
