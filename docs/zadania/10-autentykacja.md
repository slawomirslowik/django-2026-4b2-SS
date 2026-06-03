# Zadanie 10: Autentykacja – tylko zalogowani użytkownicy mogą głosować

## Cel
Zabezpiecz widok `vote` dekoratorem `@login_required`. Skonfiguruj strony logowania i wylogowania.

---

## Instrukcja krok po kroku

### Krok 1: Dodaj dekorator `@login_required` do widoku `vote`

Otwórz `polls/views.py`:

```python
from django.contrib.auth.decorators import login_required

@login_required
def vote(request, question_id):
    # ... reszta kodu bez zmian
```

Teraz niezalogowany użytkownik zostanie automatycznie przekierowany na stronę logowania.

---

### Krok 2: Skonfiguruj URL logowania

Django ma wbudowane widoki logowania/wylogowania. Otwórz `mysite/urls.py` i dodaj:

```python
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
```

---

### Krok 3: Utwórz szablon logowania

Utwórz katalog `templates/registration/` w katalogu projektu (`myproject/templates/registration/`).

Utwórz plik `login.html`:

```html
<h2>Logowanie</h2>

{% if form.errors %}
    <p style="color:red">Nieprawidłowy login lub hasło.</p>
{% endif %}

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Zaloguj się</button>
</form>
```

---

### Krok 4: Skonfiguruj katalog szablonów w `settings.py`

Upewnij się, że `TEMPLATES` w `settings.py` wskazuje na katalog szablonów projektu:

```python
TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'templates'],
        ...
    },
]
```

---

### Krok 5: Ustaw przekierowanie po zalogowaniu

W `settings.py` dodaj:

```python
LOGIN_REDIRECT_URL = '/polls/'
LOGOUT_REDIRECT_URL = '/polls/'
```

---

### Krok 6: Dodaj linki logowania/wylogowania w szablonie

W `index.html` dodaj:

```html
{% if user.is_authenticated %}
    Zalogowany jako {{ user.username }}
    <a href="{% url 'logout' %}">Wyloguj</a>
{% else %}
    <a href="{% url 'login' %}">Zaloguj się</a>
{% endif %}
```

---

### Krok 7: Przetestuj

1. Wejdź na `http://127.0.0.1:8000/polls/`
2. Kliknij link do głosowania – zostaniesz przekierowany na stronę logowania
3. Zaloguj się jako superuser
4. Sprawdź czy teraz możesz głosować

---

## Rozwiązanie – pełny kod

### `polls/views.py` (fragment)

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice


@login_required
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

### `mysite/settings.py` (dodatkowe wpisy)

```python
LOGIN_REDIRECT_URL = '/polls/'
LOGOUT_REDIRECT_URL = '/polls/'
```

### `templates/registration/login.html`

```html
<!DOCTYPE html>
<html>
<head><title>Logowanie</title></head>
<body>
<h2>Zaloguj się</h2>

{% if form.errors %}
    <p style="color:red">Nieprawidłowy login lub hasło. Spróbuj ponownie.</p>
{% endif %}

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Zaloguj się</button>
</form>
</body>
</html>
```
