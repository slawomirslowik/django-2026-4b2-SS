# Zadanie 18: Wielojęzyczność (i18n) – tłumaczenia interfejsu

## Cel
Dodaj obsługę wielojęzyczności do aplikacji `polls` używając Django Internationalization (i18n). Stwórz wersję polską i angielską interfejsu.

---

## Instrukcja krok po kroku

### Krok 1: Skonfiguruj `settings.py`

```python
from django.utils.translation import gettext_lazy as _

LANGUAGE_CODE = 'pl'  # domyślny język

USE_I18N = True
USE_L10N = True

LANGUAGES = [
    ('pl', _('Polish')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

MIDDLEWARE = [
    # ... istniejące middleware
    'django.middleware.locale.LocaleMiddleware',  # <-- dodaj po SessionMiddleware
    # ...
]
```

---

### Krok 2: Oznacz teksty do tłumaczenia w widokach

Otwórz `polls/views.py` i użyj `gettext_lazy`:

```python
from django.utils.translation import gettext_lazy as _

# Przykład użycia w widoku
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': _("Nie wybrano odpowiedzi."),
        })
    # ...
```

---

### Krok 3: Oznacz teksty w szablonach

W szablonach użyj tagu `{% trans %}`:

```html
{% load i18n %}

<h1>{% trans "Lista pytań" %}</h1>

{% for question in latest_question_list %}
    <li>
        <a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a>
    </li>
{% empty %}
    <li>{% trans "Brak pytań." %}</li>
{% endfor %}

<input type="submit" value="{% trans 'Głosuj' %}">
```

Dla dłuższych bloków tekstu użyj `{% blocktrans %}`:

```html
{% blocktrans with count=question.choice_set.count %}
    To pytanie ma {{ count }} odpowiedź.
{% endblocktrans %}
```

---

### Krok 4: Utwórz katalog locale i wygeneruj pliki tłumaczeń

Utwórz katalog:
```
mkdir myproject\locale
```

Wygeneruj plik `.po` dla języka angielskiego:
```
cd myproject
py manage.py makemessages -l en
```

> Wymaga zainstalowanego programu `gettext`. Na Windows pobierz z https://mlocati.github.io/articles/gettext-iconv-windows.html

---

### Krok 5: Wypełnij tłumaczenia

Otwórz plik `locale/en/LC_MESSAGES/django.po` i uzupełnij tłumaczenia:

```
msgid "Lista pytań"
msgstr "Question list"

msgid "Brak pytań."
msgstr "No questions available."

msgid "Głosuj"
msgstr "Vote"

msgid "Nie wybrano odpowiedzi."
msgstr "You didn't select a choice."
```

---

### Krok 6: Skompiluj tłumaczenia

```
py manage.py compilemessages
```

---

### Krok 7: Dodaj przełącznik języka w szablonie

W `base.html` dodaj formularz przełącznika języka:

```html
{% load i18n %}

<form action="{% url 'set_language' %}" method="post">
    {% csrf_token %}
    <input name="next" type="hidden" value="{{ request.get_full_path }}">
    <select name="language" onchange="this.form.submit()">
        {% get_current_language as LANGUAGE_CODE %}
        {% get_available_languages as LANGUAGES %}
        {% for lang_code, lang_name in LANGUAGES %}
            <option value="{{ lang_code }}"
                {% if lang_code == LANGUAGE_CODE %}selected{% endif %}>
                {{ lang_name }}
            </option>
        {% endfor %}
    </select>
</form>
```

---

### Krok 8: Dodaj URL przełącznika języka

W `mysite/urls.py`:

```python
from django.conf.urls.i18n import i18n_patterns
import django.conf.urls.i18n as i18n_url

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    # ... reszta URL
]
```

---

## Podsumowanie – pliki do modyfikacji

| Plik | Zmiany |
|---|---|
| `mysite/settings.py` | `LANGUAGES`, `LOCALE_PATHS`, `LocaleMiddleware` |
| `polls/views.py` | Import i użycie `gettext_lazy` |
| `polls/templates/polls/*.html` | `{% load i18n %}`, `{% trans %}` |
| `locale/en/LC_MESSAGES/django.po` | Tłumaczenia angielskie |
| `mysite/urls.py` | URL dla `i18n` |

---

## Uruchomienie z innym językiem

Możesz przetestować zmianę języka przez URL z prefixem (jeśli używasz `i18n_patterns`):
- `http://127.0.0.1:8000/pl/polls/` – wersja polska
- `http://127.0.0.1:8000/en/polls/` – wersja angielska
