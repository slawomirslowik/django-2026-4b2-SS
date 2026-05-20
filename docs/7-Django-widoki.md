# Zadanie: Dodanie widoków do aplikacji polls (Django Tutorial cz. 3 i 4)

Na podstawie oficjalnych tutoriali Django:
- https://docs.djangoproject.com/en/6.0/intro/tutorial03/
- https://docs.djangoproject.com/en/6.0/intro/tutorial04/

---

## Cel zadania

Rozbuduj aplikację `polls` o widoki obsługujące listę pytań, szczegóły pytania, głosowanie oraz wyniki. Skorzystaj z widoków opartych na funkcjach oraz klasach.

---

## Krok 1: Utwórz widoki opierając się na funkcjach

1. Otwórz plik `polls/views.py`.
2. Dodaj widoki:
   - `index` – wyświetla listę ostatnich pytań.
   - `detail` – wyświetla szczegóły wybranego pytania.
   - `results` – wyświetla wyniki głosowania dla pytania.
   - `vote` – obsługuje głosowanie na odpowiedź.

---

## Krok 2: Skonfiguruj adresy URL

1. Otwórz plik `polls/urls.py`.
2. Dodaj ścieżki do nowych widoków:
   - `/polls/` – lista pytań (index)
   - `/polls/<int:question_id>/` – szczegóły pytania (detail)
   - `/polls/<int:question_id>/results/` – wyniki (results)
   - `/polls/<int:question_id>/vote/` – głosowanie (vote)

---

## Krok 3: Utwórz szablony HTML

1. W katalogu `polls` utwórz folder `templates/polls/`.
2. Dodaj pliki szablonów:
   - `index.html` – lista pytań
   - `detail.html` – szczegóły pytania
   - `results.html` – wyniki głosowania

---

## Krok 4: Przepisz widoki na widoki generyczne (oparte o klasy z pakietu django.views.generic) - opcjonalnie

1. W pliku `polls/views.py` utwórz widoki dziedziczące po `ListView` i `DetailView`.
2. Zmień odpowiednio konfigurację URLi, aby korzystały z widoków klasowych.

---

## Krok 5: Przetestuj działanie aplikacji

1. Uruchom serwer deweloperski:
   ```
   py manage.py runserver
   ```
2. Przejdź do adresu `http://127.0.0.1:8000/polls/` i sprawdź działanie wszystkich widoków.

---

## Zadanie dodatkowe

Dodaj własny widok, który wyświetli wszystkie pytania z danej kategorii (jeśli masz model Category).

---

## Dokładne kroki do wykonania zadania (ze szczegółowym kodem)

1. **Widoki w `polls/views.py`:**

```python
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice

# Lista pytań
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# Szczegóły pytania
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

# Wyniki głosowania
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

# Głosowanie
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Nie wybrano odpowiedzi.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
```

2. **Adresy URL w `polls/urls.py`:**

```python
from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
```

3. **Szablony HTML w `polls/templates/polls/`:**

- `index.html`:

```html
<h1>Lista pytań</h1>
<ul>
{% for question in latest_question_list %}
    <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
{% empty %}
    <li>Brak pytań.</li>
{% endfor %}
</ul>
```

- `detail.html`:

```html
<h1>{{ question.question_text }}</h1>
{% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
<form action="{% url 'polls:vote' question.id %}" method="post">
{% csrf_token %}
{% for choice in question.choice_set.all %}
    <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
    <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
{% endfor %}
<input type="submit" value="Głosuj">
</form>
```

- `results.html`:

```html
<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} — {{ choice.votes }} głosów</li>
{% endfor %}
</ul>
<a href="{% url 'polls:detail' question.id %}">Głosuj ponownie</a>
```

4. **(Opcjonalnie) Widoki klasowe:**

```python
from django.views import generic

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
```

W `urls.py`:

```python
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
```

5. **Uruchom serwer poleceniem:**

```
py manage.py runserver
```

6. **Sprawdź w przeglądarce adresy:**
   - `http://127.0.0.1:8000/polls/` (lista pytań)
   - `http://127.0.0.1:8000/polls/<id>/` (szczegóły pytania)
   - `http://127.0.0.1:8000/polls/<id>/results/` (wyniki)
   - `http://127.0.0.1:8000/polls/<id>/vote/` (głosowanie)

7. **(Dla zadania dodatkowego)** Dodaj widok wyświetlający pytania z danej kategorii i odpowiedni szablon.

---



**Pamiętaj, aby po każdej zmianie w kodzie zapisać pliki i odświeżyć stronę w przeglądarce oraz na zakończenie wykonać commit i push do repozytorium githuba.**
