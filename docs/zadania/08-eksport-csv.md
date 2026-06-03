# Zadanie 8: Eksport wyników głosowania do CSV

## Cel
Stwórz widok, który eksportuje wyniki głosowania dla wybranego pytania do pliku CSV.

---

## Instrukcja krok po kroku

### Krok 1: Dodaj widok eksportu CSV

Django nie ma wbudowanego eksportu CSV, ale Python ma moduł `csv` w bibliotece standardowej. Otwórz `polls/views.py` i dodaj:

```python
import csv
from django.http import HttpResponse

def export_results_csv(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # Utwórz odpowiedź HTTP z nagłówkiem CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="wyniki_{question_id}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Odpowiedź', 'Liczba głosów'])  # nagłówki

    for choice in question.choice_set.all():
        writer.writerow([choice.choice_text, choice.votes])

    return response
```

**Wyjaśnienie:**
- `content_type='text/csv'` – mówi przeglądarce, że to plik CSV
- `Content-Disposition: attachment` – powoduje pobranie pliku zamiast wyświetlenia
- `csv.writer(response)` – zapisuje dane CSV bezpośrednio do odpowiedzi HTTP

---

### Krok 2: Dodaj URL

W `polls/urls.py`:

```python
path('<int:question_id>/export/', views.export_results_csv, name='export_csv'),
```

---

### Krok 3: Dodaj link w szablonie `results.html`

```html
<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} — {{ choice.votes }} głosów</li>
{% endfor %}
</ul>

<a href="{% url 'polls:export_csv' question.id %}">Pobierz wyniki jako CSV</a>
<a href="{% url 'polls:detail' question.id %}">Głosuj ponownie</a>
```

---

### Krok 4: Przetestuj

1. Zagłosuj na kilka pytań
2. Przejdź do wyników (`/polls/<id>/results/`)
3. Kliknij „Pobierz wyniki jako CSV"
4. Otwórz plik w Excelu lub edytorze tekstowym

---

## Rozwiązanie – pełny kod

### `polls/views.py` (nowy widok)

```python
import csv
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Question


def export_results_csv(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="wyniki_pytanie_{question_id}.csv"'

    # BOM dla poprawnego wyświetlania polskich znaków w Excelu
    response.write('\ufeff')

    writer = csv.writer(response)
    writer.writerow(['Pytanie', question.question_text])
    writer.writerow(['Data publikacji', question.pub_date.strftime('%d.%m.%Y')])
    writer.writerow([])
    writer.writerow(['Odpowiedź', 'Liczba głosów', '% głosów'])

    total = sum(c.votes for c in question.choice_set.all())
    for choice in question.choice_set.all():
        percent = round(choice.votes / total * 100, 1) if total > 0 else 0
        writer.writerow([choice.choice_text, choice.votes, f'{percent}%'])

    writer.writerow([])
    writer.writerow(['Łącznie', total, '100%'])

    return response
```
