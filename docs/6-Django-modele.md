# Django: Modele – Manual i Zadania (na podstawie tutoriala cz. 2)

Źródło: [Django Tutorial cz. 2 – Modele](https://docs.djangoproject.com/en/6.0/intro/tutorial02/)

---

## Do czego służy model w Django?

Model w Django jest klasą Python, która reprezentuje strukturę danych (np. tabelę w bazie danych). Model określa jakie pola i typy danych będą przechowywane, a Django automatycznie tworzy odpowiednie tabele w bazie na podstawie tych klas. Modele pozwalają na:
- definiowanie struktury danych,
- wykonywanie operacji CRUD (tworzenie, odczyt, aktualizacja, usuwanie),
- mapowanie obiektów Python na rekordy w bazie danych.

---

## Instrukcja: Dodanie modeli Question i Choice

### 1. Otwórz plik `polls/models.py`

### 2. Dodaj model Question:

```python
from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text
```

### 2a. Dodaj metodę was_published_recently do modelu Question:

Ta metoda pozwala sprawdzić, czy pytanie zostało opublikowane w ciągu ostatnich 24 godzin.

```python
import datetime
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text
```

### 3. Dodaj model Choice:

```python
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
```

### 4. Zapisz plik.

---

### 5. Utwórz migracje dla nowych modeli:

W terminalu, będąc w katalogu projektu, uruchom:

```
py manage.py makemigrations polls
```

---

### 6. Zastosuj migracje (utwórz tabele w bazie):

```
py manage.py migrate
```

---

### 7. Sprawdź, czy modele zostały poprawnie dodane:

Możesz użyć polecenia:

```
py manage.py shell
```

W konsoli Pythona:

```python
from polls.models import Question, Choice
Question.objects.all()
Choice.objects.all()
```

---

## Tworzenie konta administratora (superuser)

Aby zarządzać danymi w panelu administracyjnym Django, utwórz konto administratora (superuser):

1. W terminalu, będąc w katalogu projektu, uruchom:

```
py manage.py createsuperuser
```

2. Podaj nazwę użytkownika, adres e-mail oraz hasło zgodnie z instrukcjami w terminalu.

3. Po utworzeniu konta możesz zalogować się do panelu admina pod adresem:

```
http://127.0.0.1:8000/admin/
```

---

## Zadanie: Stwórz własny model

1. W pliku `polls/models.py` dodaj własny model `Category`, który będzie grupował poszczególne pytania (`Questions`).

2. Utwórz migracje.

3. Zastosuj migracje.

4. Sprawdź w konsoli Pythona, czy model działa poprawnie.

---

**Nie podawaj od razu rozwiązania – spróbuj samodzielnie zaprojektować model Category oraz powiązanie z Question.**

---

**Manual oraz zadanie przygotowane zgodnie z tutorialem Django cz. 2.**