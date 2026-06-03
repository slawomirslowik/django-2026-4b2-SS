# Zadanie 2: Stronicowanie listy pytań (Paginator)

## Cel
Ogranicz listę pytań do 5 na stronę używając Django Paginator. Dodaj nawigację między stronami w szablonie.

---

## Instrukcja krok po kroku

### Krok 1: Zaktualizuj widok `IndexView`

Otwórz `polls/views.py`. Jeśli używasz widoku generycznego `ListView`, stronicowanie możesz włączyć jedną linią:

```python
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    paginate_by = 5  # <-- dodaj tę linię

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')
```

`ListView` automatycznie obsługuje parametr `?page=2` w URL i przekazuje do szablonu obiekt `page_obj`.

---

### Krok 2: Zaktualizuj szablon `index.html`

Dodaj nawigację paginacji na dole szablonu:

```html
<h1>Lista pytań</h1>
<ul>
{% for question in latest_question_list %}
    <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a>
        <small>{{ question.pub_date }}</small>
    </li>
{% empty %}
    <li>Brak pytań.</li>
{% endfor %}
</ul>

<!-- Nawigacja paginacji -->
<div class="pagination">
    <span class="step-links">
        {% if page_obj.has_previous %}
            <a href="?page=1">&laquo; pierwsza</a>
            <a href="?page={{ page_obj.previous_page_number }}">poprzednia</a>
        {% endif %}

        <span class="current">
            Strona {{ page_obj.number }} z {{ page_obj.paginator.num_pages }}
        </span>

        {% if page_obj.has_next %}
            <a href="?page={{ page_obj.next_page_number }}">następna</a>
            <a href="?page={{ page_obj.paginator.num_pages }}">ostatnia &raquo;</a>
        {% endif %}
    </span>
</div>
```

---

### Krok 3: Dodaj dane testowe

Aby przetestować paginację, utwórz kilkanaście pytań przez panel admina lub shell:

```python
# py manage.py shell
import datetime
from django.utils import timezone
from polls.models import Question

for i in range(1, 20):
    Question.objects.create(
        question_text=f"Pytanie testowe nr {i}?",
        pub_date=timezone.now() - datetime.timedelta(days=i)
    )
```

---

### Krok 4: Przetestuj

Wejdź na `http://127.0.0.1:8000/polls/` – powinna wyświetlić się pierwsza strona z 5 pytaniami i linki nawigacji.

---

## Rozwiązanie – pełny kod

### `polls/views.py` (fragment)

```python
from django.utils import timezone
from django.views import generic
from .models import Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    paginate_by = 5

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')
```

### `polls/templates/polls/index.html`

```html
<h1>Lista pytań</h1>
<ul>
{% for question in latest_question_list %}
    <li>
        <a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a>
        <small>({{ question.pub_date|date:"d.m.Y" }})</small>
    </li>
{% empty %}
    <li>Brak pytań.</li>
{% endfor %}
</ul>

<div>
    {% if page_obj.has_previous %}
        <a href="?page={{ page_obj.previous_page_number }}">&laquo; Poprzednia</a>
    {% endif %}

    Strona {{ page_obj.number }} z {{ page_obj.paginator.num_pages }}

    {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}">Następna &raquo;</a>
    {% endif %}
</div>
```
