# Zadanie 12: AJAX – głosowanie bez przeładowania strony

## Cel
Przebuduj formularz głosowania tak, aby działał przez AJAX (Fetch API) – wynik głosowania wyświetli się bez przeładowania strony.

---

## Wymagania wstępne
- Aplikacja `polls` z widokami i szablonami
- Podstawowa znajomość JavaScript

---

## Instrukcja krok po kroku

### Krok 1: Zmodyfikuj widok `vote` – zwróć JSON

Zmień widok `vote` tak, aby zwracał odpowiedź JSON zamiast przekierowania:

```python
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@require_POST
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST.get('choice'))
    except (KeyError, Choice.DoesNotExist):
        return JsonResponse({'status': 'error', 'message': 'Nie wybrano odpowiedzi.'}, status=400)

    selected_choice.votes += 1
    selected_choice.save()

    # Zwróć zaktualizowane wyniki
    choices_data = [
        {'id': c.id, 'choice_text': c.choice_text, 'votes': c.votes}
        for c in question.choice_set.all()
    ]
    return JsonResponse({'status': 'ok', 'choices': choices_data})
```

---

### Krok 2: Zaktualizuj szablon `detail.html`

Dodaj JavaScript obsługujący AJAX:

```html
<h1>{{ question.question_text }}</h1>

<div id="error-message" class="error" style="display:none; color:red;"></div>
<div id="success-message" style="display:none; color:green;"></div>

<form id="vote-form">
    {% csrf_token %}
    {% for choice in question.choice_set.all %}
        <div>
            <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
            <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label>
        </div>
    {% endfor %}
    <button type="submit">Głosuj</button>
</form>

<div id="results" style="display:none;">
    <h2>Aktualne wyniki:</h2>
    <ul id="results-list"></ul>
</div>

<script>
document.getElementById('vote-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);
    const csrfToken = formData.get('csrfmiddlewaretoken');
    const choice = formData.get('choice');

    fetch("{% url 'polls:vote' question.id %}", {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `choice=${choice}&csrfmiddlewaretoken=${csrfToken}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok') {
            document.getElementById('error-message').style.display = 'none';
            document.getElementById('success-message').textContent = 'Głos oddany!';
            document.getElementById('success-message').style.display = 'block';
            document.getElementById('vote-form').style.display = 'none';

            const resultsList = document.getElementById('results-list');
            resultsList.innerHTML = '';
            data.choices.forEach(choice => {
                const li = document.createElement('li');
                li.textContent = `${choice.choice_text}: ${choice.votes} głosów`;
                resultsList.appendChild(li);
            });
            document.getElementById('results').style.display = 'block';
        } else {
            document.getElementById('error-message').textContent = data.message;
            document.getElementById('error-message').style.display = 'block';
        }
    })
    .catch(error => {
        console.error('Błąd:', error);
    });
});
</script>
```

---

### Krok 3: Przetestuj

1. Wejdź na stronę szczegółów pytania
2. Wybierz odpowiedź i kliknij „Głosuj"
3. Wyniki powinny pojawić się bez przeładowania strony

---

## Rozwiązanie – pełny widok `vote`

```python
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .models import Question, Choice


@require_POST
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choice_id = request.POST.get('choice')

    if not choice_id:
        return JsonResponse(
            {'status': 'error', 'message': 'Nie wybrano odpowiedzi.'},
            status=400
        )

    try:
        selected_choice = question.choice_set.get(pk=choice_id)
    except Choice.DoesNotExist:
        return JsonResponse(
            {'status': 'error', 'message': 'Nieprawidłowa odpowiedź.'},
            status=400
        )

    selected_choice.votes += 1
    selected_choice.save()

    choices_data = [
        {'id': c.id, 'choice_text': c.choice_text, 'votes': c.votes}
        for c in question.choice_set.order_by('-votes')
    ]
    return JsonResponse({'status': 'ok', 'choices': choices_data})
```
