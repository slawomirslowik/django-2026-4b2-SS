# Zadanie 3: Licznik głosów na liście pytań

## Cel
Wyświetl przy każdym pytaniu na liście łączną liczbę oddanych głosów ze wszystkich odpowiedzi.

---

## Instrukcja krok po kroku

### Krok 1: Zaktualizuj widok `IndexView`

Użyj adnotacji ORM (`annotate`) do obliczenia sumy głosów dla każdego pytania bezpośrednio w zapytaniu do bazy danych.

Otwórz `polls/views.py` i zmodyfikuj `get_queryset`:

```python
from django.db.models import Sum
from django.utils import timezone
from django.views import generic
from .models import Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).annotate(
            total_votes=Sum('choice__votes')
        ).order_by('-pub_date')
```

Dzięki `annotate` każdy obiekt `Question` w szablonie będzie miał dodatkowe pole `total_votes`.

---

### Krok 2: Zaktualizuj szablon `index.html`

```html
<h1>Lista pytań</h1>
<ul>
{% for question in latest_question_list %}
    <li>
        <a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a>
        –
        {% if question.total_votes %}
            {{ question.total_votes }} głosów
        {% else %}
            Brak głosów
        {% endif %}
    </li>
{% empty %}
    <li>Brak pytań.</li>
{% endfor %}
</ul>
```

---

### Krok 3: Przetestuj

1. Zagłosuj kilka razy na różne pytania
2. Wejdź na `http://127.0.0.1:8000/polls/`
3. Sprawdź czy liczby głosów są poprawne

---

## Rozwiązanie – pełny kod

### `polls/views.py`

```python
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).annotate(
            total_votes=Sum('choice__votes')
        ).order_by('-pub_date')
```

### `polls/templates/polls/index.html`

```html
<h1>Ankiety</h1>
<ul>
{% for question in latest_question_list %}
    <li>
        <a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a>
        <em>({{ question.total_votes|default:"0" }} głosów)</em>
    </li>
{% empty %}
    <li>Brak pytań.</li>
{% endfor %}
</ul>
```
