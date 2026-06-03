# Zadanie 4: Ochrona przed wielokrotnym głosowaniem (sesje)

## Cel
Zabezpiecz widok `vote` tak, aby użytkownik mógł zagłosować na dane pytanie tylko raz. Wykorzystaj mechanizm sesji Django.

---

## Instrukcja krok po kroku

### Krok 1: Jak działają sesje w Django?

Django przechowuje dane sesji po stronie serwera i identyfikuje użytkownika za pomocą ciasteczka `sessionid`. Możesz zapisywać i odczytywać dane sesji przez `request.session` jak ze słownika.

---

### Krok 2: Zaktualizuj widok `vote`

Otwórz `polls/views.py` i zmień widok `vote`:

```python
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # Sprawdź czy użytkownik już głosował
    voted_questions = request.session.get('voted_questions', [])
    if question_id in voted_questions:
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Już głosowałeś na to pytanie.",
        })

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

        # Zapisz w sesji informację o oddaniu głosu
        voted_questions.append(question_id)
        request.session['voted_questions'] = voted_questions

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
```

---

### Krok 3: Zaktualizuj szablon `detail.html`

Dodaj informację o błędzie w szablonie (jeśli jeszcze nie ma):

```html
<h1>{{ question.question_text }}</h1>

{% if error_message %}
    <p style="color: red;"><strong>{{ error_message }}</strong></p>
{% endif %}

<form action="{% url 'polls:vote' question.id %}" method="post">
{% csrf_token %}
{% for choice in question.choice_set.all %}
    <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
    <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
{% endfor %}
<input type="submit" value="Głosuj">
</form>
```

---

### Krok 4: Przetestuj

1. Zagłosuj na pytanie
2. Wróć na stronę pytania i spróbuj zagłosować ponownie
3. Powinien pojawić się komunikat "Już głosowałeś na to pytanie."

---

## Rozwiązanie – pełny kod widoku `vote`

```python
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    voted_questions = request.session.get('voted_questions', [])
    if question_id in voted_questions:
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Już głosowałeś na to pytanie.",
        })

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
        voted_questions.append(question_id)
        request.session['voted_questions'] = voted_questions
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
```
