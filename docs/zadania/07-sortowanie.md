# Zadanie 7: Sortowanie pytań

## Cel
Dodaj możliwość sortowania listy pytań po dacie publikacji lub łącznej liczbie głosów, wybieranego przez użytkownika.

---

## Instrukcja krok po kroku

### Krok 1: Zmień `IndexView` na widok funkcyjny

Sortowanie dynamiczne (na podstawie parametru GET) jest łatwiejsze w widoku funkcyjnym. Zmień `IndexView` na:

```python
from django.db.models import Sum

def index(request):
    sort = request.GET.get('sort', 'date')  # domyślnie sortuj po dacie

    questions = Question.objects.filter(
        pub_date__lte=timezone.now()
    ).annotate(total_votes=Sum('choice__votes'))

    if sort == 'votes':
        questions = questions.order_by('-total_votes')
    else:
        questions = questions.order_by('-pub_date')

    return render(request, 'polls/index.html', {
        'latest_question_list': questions,
        'current_sort': sort,
    })
```

---

### Krok 2: Zaktualizuj URL

W `polls/urls.py` zmień wpis dla index:

```python
path('', views.index, name='index'),
```

---

### Krok 3: Zaktualizuj szablon `index.html`

Dodaj przyciski sortowania:

```html
<h1>Lista pytań</h1>

<p>
    Sortuj:
    <a href="?sort=date" {% if current_sort == 'date' %}style="font-weight:bold"{% endif %}>
        Po dacie
    </a> |
    <a href="?sort=votes" {% if current_sort == 'votes' %}style="font-weight:bold"{% endif %}>
        Po liczbie głosów
    </a>
</p>

<ul>
{% for question in latest_question_list %}
    <li>
        <a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a>
        – {{ question.total_votes|default:"0" }} głosów
        ({{ question.pub_date|date:"d.m.Y" }})
    </li>
{% empty %}
    <li>Brak pytań.</li>
{% endfor %}
</ul>
```

---

### Krok 4: Przetestuj

1. Wejdź na `http://127.0.0.1:8000/polls/`
2. Kliknij „Po dacie" i „Po liczbie głosów"
3. Sprawdź czy kolejność pytań się zmienia

---

## Rozwiązanie – pełny kod

### `polls/views.py`

```python
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone
from .models import Question


def index(request):
    sort = request.GET.get('sort', 'date')

    questions = Question.objects.filter(
        pub_date__lte=timezone.now()
    ).annotate(total_votes=Sum('choice__votes'))

    if sort == 'votes':
        questions = questions.order_by('-total_votes')
    else:
        questions = questions.order_by('-pub_date')

    return render(request, 'polls/index.html', {
        'latest_question_list': questions,
        'current_sort': sort,
    })
```

### `polls/templates/polls/index.html`

```html
<h1>Ankiety</h1>

<p>
    Sortuj po:
    <a href="?sort=date"><strong>{% if current_sort == 'date' %}[Data]{% else %}Dacie{% endif %}</strong></a> |
    <a href="?sort=votes"><strong>{% if current_sort == 'votes' %}[Głosy]{% else %}Głosach{% endif %}</strong></a>
</p>

<ul>
{% for question in latest_question_list %}
    <li>
        <a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a>
        <em>{{ question.total_votes|default:"0" }} głosów – {{ question.pub_date|date:"d.m.Y" }}</em>
    </li>
{% empty %}
    <li>Brak pytań.</li>
{% endfor %}
</ul>
```
