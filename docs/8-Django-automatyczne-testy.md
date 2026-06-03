# Django: Automatyczne testy aplikacji (Tutorial cz. 5)

Źródło: [https://docs.djangoproject.com/pl/6.0/intro/tutorial05/](https://docs.djangoproject.com/pl/6.0/intro/tutorial05/)

---

## Czym są zautomatyzowane testy?

Testy są rutynami, które sprawdzają działanie kodu. Zautomatyzowane testy różnią się od testów ręcznych tym, że system wykonuje je za programistę. Wystarczy raz napisać zestaw testów i uruchamiać je automatycznie po każdej zmianie kodu.

### Dlaczego warto pisać testy?

- **Oszczędzają czas** – zamiast ręcznie sprawdzać dziesiątki scenariuszy, testy robią to w sekundy.
- **Pomagają unikać błędów** – oświetlają kod z wnętrza i natychmiast sygnalizują, gdy coś pójdzie nie tak.
- **Kod z testami jest bardziej atrakcyjny** – „Kod bez testów jest popsuty z założenia" (Jacob Kaplan-Moss).
- **Ułatwiają pracę zespołową** – gwarantują, że współpracownicy nie psują przypadkowo Twojego kodu.

---

## Krok 1: Odnajdź błąd w metodzie `was_published_recently()`

Metoda `was_published_recently()` zwraca `True` dla pytań z datą w **przyszłości** – co jest błędem. Sprawdź to w shellu:

```
py manage.py shell
```

```python
import datetime
from django.utils import timezone
from polls.models import Question

future_question = Question(pub_date=timezone.now() + datetime.timedelta(days=30))
future_question.was_published_recently()  # Zwraca True – to błąd!
```

---

## Krok 2: Napisz test wskazujący błąd

Otwórz plik `polls/tests.py` i dodaj:

```python
import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() zwraca False dla pytań z pub_date w przyszłości.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
```

---

## Krok 3: Uruchom testy

```
py manage.py test polls
```

Test powinien zakończyć się niepowodzeniem (FAIL) – to potwierdza obecność błędu.

---

## Krok 4: Napraw błąd w modelu

Otwórz `polls/models.py` i popraw metodę `was_published_recently()`:

```python
import datetime
from django.utils import timezone

def was_published_recently(self):
    now = timezone.now()
    return now - datetime.timedelta(days=1) <= self.pub_date <= now
```

Uruchom testy ponownie – tym razem powinny przejść (OK).

---

## Krok 5: Dodaj więcej testów modelu

Przetestuj wszystkie przypadki metody `was_published_recently()`:

```python
def test_was_published_recently_with_old_question(self):
    """
    was_published_recently() zwraca False dla pytań starszych niż 1 dzień.
    """
    time = timezone.now() - datetime.timedelta(days=1, seconds=1)
    old_question = Question(pub_date=time)
    self.assertIs(old_question.was_published_recently(), False)


def test_was_published_recently_with_recent_question(self):
    """
    was_published_recently() zwraca True dla pytań z ostatnich 24 godzin.
    """
    time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    recent_question = Question(pub_date=time)
    self.assertIs(recent_question.was_published_recently(), True)
```

---

## Krok 6: Popraw widok – wykluczenie przyszłych pytań

Otwórz `polls/views.py` i zaktualizuj `IndexView`, aby nie pokazywał pytań z przyszłą datą:

```python
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Zwraca ostatnie 5 pytań (bez tych z pub_date w przyszłości).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
```

---

## Krok 7: Przetestuj widok IndexView

Dodaj do `polls/tests.py` funkcję pomocniczą i klasę testów widoku:

```python
from django.urls import reverse


def create_question(question_text, days):
    """
    Tworzy pytanie z podanym tekstem i przesunięciem daty (ujemne = przeszłość, dodatnie = przyszłość).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """Jeśli nie ma pytań, wyświetla odpowiedni komunikat."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brak pytań.")
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Pytania z przeszłości są widoczne na stronie głównej."""
        question = create_question(question_text="Pytanie z przeszłości.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [question])

    def test_future_question(self):
        """Pytania z przyszłością NIE są wyświetlane."""
        create_question(question_text="Pytanie z przyszłości.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "Brak pytań.")
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_question(self):
        """Jeśli istnieją oba, widoczne jest tylko pytanie z przeszłości."""
        question = create_question(question_text="Pytanie z przeszłości.", days=-30)
        create_question(question_text="Pytanie z przyszłości.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [question])

    def test_two_past_questions(self):
        """Strona może wyświetlić kilka pytań."""
        q1 = create_question(question_text="Pytanie 1.", days=-30)
        q2 = create_question(question_text="Pytanie 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [q2, q1])
```

---

## Krok 8: Przetestuj widok DetailView

Zaktualizuj `DetailView` w `polls/views.py`, aby blokował dostęp do przyszłych pytań:

```python
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Wyklucza pytania, które nie są jeszcze opublikowane."""
        return Question.objects.filter(pub_date__lte=timezone.now())
```

Dodaj testy widoku `DetailView`:

```python
class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """Widok szczegółów dla pytania z przyszłością zwraca 404."""
        future_question = create_question(question_text="Pytanie z przyszłości.", days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """Widok szczegółów dla pytania z przeszłości wyświetla treść pytania."""
        past_question = create_question(question_text="Pytanie z przeszłości.", days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
```

---

## Krok 9: Uruchom wszystkie testy

```
py manage.py test polls
```

---

## Dobre praktyki organizacji testów

- Osobna klasa `TestCase` dla każdego modelu i każdego widoku.
- Osobna metoda testowa dla każdego zestawu warunków.
- Nazwy metod testowych opisują, co testują (np. `test_future_question_returns_404`).
- Im więcej testów, tym lepiej – redundancja w testach jest zaletą, nie wadą.

---

## Zadania

### Zadanie 1
Napisz test sprawdzający, że `was_published_recently()` zwraca `False` dla pytania opublikowanego dokładnie 2 dni temu.

### Zadanie 2
Dodaj metodę `get_queryset()` do `ResultsView` (analogicznie jak w `DetailView`), która wyklucza pytania z przyszłą datą, i napisz odpowiednie testy.

### Zadanie 3
Napisz test sprawdzający, że pytanie bez żadnych odpowiedzi (`Choice`) nie jest wyświetlane na liście pytań.

### Zadanie 4
Napisz test sprawdzający, że widok `results` zwraca 404 dla pytania z `pub_date` w przyszłości.

### Zadanie 5
Napisz test sprawdzający poprawność liczby głosów po oddaniu głosu przez widok `vote`.

---

**Dokumentacja Django – testowanie:** [https://docs.djangoproject.com/pl/6.0/topics/testing/](https://docs.djangoproject.com/pl/6.0/topics/testing/)
