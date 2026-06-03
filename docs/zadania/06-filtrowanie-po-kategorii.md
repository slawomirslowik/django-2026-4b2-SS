# Zadanie 6: Filtrowanie pytań po kategorii

## Cel
Dodaj możliwość filtrowania listy pytań według kategorii (`Category`) przez parametr w URL.

---

## Instrukcja krok po kroku

### Krok 1: Upewnij się, że model Category istnieje

W `polls/models.py` powinien istnieć model:

```python
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
```

Oraz `Question` powinien mieć pole:

```python
category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
```

---

### Krok 2: Dodaj widok filtrowania

Otwórz `polls/views.py` i dodaj widok:

```python
def by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    questions = Question.objects.filter(
        category=category,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')
    categories = Category.objects.all()
    return render(request, 'polls/by_category.html', {
        'category': category,
        'questions': questions,
        'categories': categories,
    })
```

---

### Krok 3: Dodaj URL

W `polls/urls.py`:

```python
path('category/<int:category_id>/', views.by_category, name='by_category'),
```

---

### Krok 4: Utwórz szablon `by_category.html`

```html
<h1>Kategoria: {{ category.name }}</h1>

<h3>Inne kategorie:</h3>
<ul>
{% for cat in categories %}
    <li><a href="{% url 'polls:by_category' cat.id %}">{{ cat.name }}</a></li>
{% endfor %}
</ul>

<h3>Pytania:</h3>
<ul>
{% for question in questions %}
    <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
{% empty %}
    <li>Brak pytań w tej kategorii.</li>
{% endfor %}
</ul>
```

---

### Krok 5: Zaktualizuj `IndexView` – dodaj listę kategorii do kontekstu

Aby wyświetlić listę kategorii na stronie głównej, nadpisz metodę `get_context_data`:

```python
from .models import Question, Category

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
```

---

### Krok 6: Dodaj listę kategorii w `index.html`

```html
<h3>Kategorie:</h3>
<ul>
{% for cat in categories %}
    <li><a href="{% url 'polls:by_category' cat.id %}">{{ cat.name }}</a></li>
{% endfor %}
</ul>
```

---

## Rozwiązanie – pełny kod

### `polls/views.py` (nowy widok)

```python
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .models import Question, Category


def by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    questions = Question.objects.filter(
        category=category,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')
    categories = Category.objects.all()
    return render(request, 'polls/by_category.html', {
        'category': category,
        'questions': questions,
        'categories': categories,
    })
```

### `polls/templates/polls/by_category.html`

```html
<h1>Kategoria: {{ category.name }}</h1>

<p><a href="{% url 'polls:index' %}">&laquo; Wróć do listy</a></p>

<h3>Wszystkie kategorie:</h3>
<ul>
{% for cat in categories %}
    <li>
        {% if cat == category %}
            <strong>{{ cat.name }}</strong>
        {% else %}
            <a href="{% url 'polls:by_category' cat.id %}">{{ cat.name }}</a>
        {% endif %}
    </li>
{% endfor %}
</ul>

<h3>Pytania w kategorii "{{ category.name }}":</h3>
<ul>
{% for question in questions %}
    <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
{% empty %}
    <li>Brak pytań w tej kategorii.</li>
{% endfor %}
</ul>
```
