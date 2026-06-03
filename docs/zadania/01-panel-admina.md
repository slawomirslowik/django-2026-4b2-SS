# Zadanie 1: Panel admina – rejestracja modeli i customizacja

## Cel
Zarejestruj modele `Question`, `Choice` i `Category` w panelu administracyjnym Django i dostosuj ich widok.

## Wymagania wstępne
- Działająca aplikacja `polls` z modelami `Question`, `Choice`, `Category`
- Utworzone konto superusera (`py manage.py createsuperuser`)

---

## Instrukcja krok po kroku

### Krok 1: Podstawowa rejestracja modeli

Otwórz plik `polls/admin.py`. Domyślnie wygląda tak:

```python
from django.contrib import admin
# Register your models here.
```

Zarejestruj wszystkie modele:

```python
from django.contrib import admin
from .models import Question, Choice, Category

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Category)
```

Wejdź na `http://127.0.0.1:8000/admin/` i sprawdź, czy modele są widoczne.

---

### Krok 2: Customizacja widoku listy `Question`

Dodaj klasę `QuestionAdmin`, która:
- pokazuje kolumny: `question_text`, `pub_date`, `was_published_recently`
- umożliwia wyszukiwanie po `question_text`
- umożliwia filtrowanie po `pub_date`

```python
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'pub_date', 'was_published_recently']
    search_fields = ['question_text']
    list_filter = ['pub_date', 'category']

admin.site.register(Question, QuestionAdmin)
```

---

### Krok 3: Inline dla Choice w Question

Dodaj możliwość edytowania odpowiedzi (`Choice`) bezpośrednio na stronie pytania:

```python
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3  # liczba pustych pól do dodania

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'pub_date', 'was_published_recently']
    search_fields = ['question_text']
    list_filter = ['pub_date', 'category']
    inlines = [ChoiceInline]
```

---

### Krok 4: Customizacja Category

```python
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

admin.site.register(Category, CategoryAdmin)
```

---

### Krok 5: Przetestuj

1. Uruchom serwer: `py manage.py runserver`
2. Wejdź na `http://127.0.0.1:8000/admin/`
3. Sprawdź czy widoczne są kolumny, wyszukiwarka i filtry
4. Dodaj nowe pytanie wraz z odpowiedziami przez inline

---

## Rozwiązanie – pełny kod `polls/admin.py`

```python
from django.contrib import admin
from .models import Question, Choice, Category


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'pub_date', 'was_published_recently', 'category']
    search_fields = ['question_text']
    list_filter = ['pub_date', 'category']
    inlines = [ChoiceInline]
    fieldsets = [
        (None, {'fields': ['question_text', 'category']}),
        ('Informacje o dacie', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Category, CategoryAdmin)
```
