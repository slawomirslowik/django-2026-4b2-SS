# Zadanie 14: Powiadomienia e-mail po przekroczeniu limitu głosów

## Cel
Wysyłaj e-mail do administratora gdy łączna liczba głosów dla pytania przekroczy zadany próg (np. 10 głosów).

---

## Instrukcja krok po kroku

### Krok 1: Skonfiguruj backend e-mail w `settings.py`

#### Opcja A: Wyświetlanie e-maili w konsoli (do testowania)

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Wiadomości pojawią się w terminalu zamiast być wysyłane.

#### Opcja B: Prawdziwy SMTP (np. Gmail)

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'twoj@gmail.com'
EMAIL_HOST_PASSWORD = 'haslo_aplikacji'  # hasło aplikacji Google, nie zwykłe hasło
DEFAULT_FROM_EMAIL = 'twoj@gmail.com'
ADMIN_EMAIL = 'admin@example.com'  # adres do powiadomień
```

> ⚠️ Nigdy nie przechowuj haseł bezpośrednio w `settings.py` – użyj zmiennych środowiskowych.

---

### Krok 2: Zaktualizuj widok `vote`

Dodaj logikę wysyłania e-maila po oddaniu głosu:

```python
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum

VOTE_THRESHOLD = 10  # próg głosów wyzwalający powiadomienie

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Nie wybrano odpowiedzi.",
        })

    selected_choice.votes += 1
    selected_choice.save()

    # Sprawdź łączną liczbę głosów
    total_votes = question.choice_set.aggregate(total=Sum('votes'))['total'] or 0

    if total_votes == VOTE_THRESHOLD:
        send_mail(
            subject=f'Ankieta "{question.question_text}" osiągnęła {VOTE_THRESHOLD} głosów!',
            message=(
                f'Pytanie: {question.question_text}\n'
                f'Łączna liczba głosów: {total_votes}\n\n'
                f'Wyniki:\n' +
                '\n'.join(
                    f'  - {c.choice_text}: {c.votes}'
                    for c in question.choice_set.all()
                )
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=True,  # nie rzucaj wyjątku jeśli wysyłka się nie powiedzie
        )

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
```

---

### Krok 3: Przetestuj z backendem konsolowym

1. Ustaw `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`
2. Zagłosuj tyle razy, aby przekroczyć próg (10)
3. Sprawdź terminal – powinien pojawić się wydruk e-maila

---

### Krok 4: Zmienne środowiskowe (bezpieczne przechowywanie danych)

Zamiast wpisywać hasło w `settings.py`, użyj zmiennych środowiskowych:

Zainstaluj `python-decouple`:
```
pip install python-decouple
```

Utwórz plik `.env` w katalogu projektu:
```
EMAIL_HOST_USER=twoj@gmail.com
EMAIL_HOST_PASSWORD=twoje_haslo_aplikacji
ADMIN_EMAIL=admin@example.com
```

W `settings.py`:
```python
from decouple import config

EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
ADMIN_EMAIL = config('ADMIN_EMAIL')
```

---

## Rozwiązanie – pełny kod

### `mysite/settings.py` (fragment)

```python
# E-mail – konsola do testowania
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@polls.local'
ADMIN_EMAIL = 'admin@polls.local'
VOTE_THRESHOLD = 10
```

### `polls/views.py` (widok vote)

```python
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST.get('choice'))
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Nie wybrano odpowiedzi.",
        })

    selected_choice.votes += 1
    selected_choice.save()

    total_votes = question.choice_set.aggregate(total=Sum('votes'))['total'] or 0
    threshold = getattr(settings, 'VOTE_THRESHOLD', 10)

    if total_votes == threshold:
        send_mail(
            subject=f'[Ankiety] Pytanie osiągnęło {threshold} głosów',
            message=(
                f'Pytanie: "{question.question_text}"\n'
                f'Łączna liczba głosów: {total_votes}\n\n'
                'Wyniki:\n' +
                '\n'.join(
                    f'  {c.choice_text}: {c.votes} głosów'
                    for c in question.choice_set.order_by('-votes')
                )
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=True,
        )

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
```
