# Zadanie 11: Stylowanie aplikacji z Bootstrap 5

## Cel
Przeprojektuj front-end aplikacji `polls` używając frameworka CSS Bootstrap 5 z CDN. Stwórz spójny, responsywny wygląd wszystkich stron.

---

## Instrukcja krok po kroku

### Krok 1: Utwórz szablon bazowy

Utwórz plik `polls/templates/polls/base.html`:

```html
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}Ankiety{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
    <div class="container">
        <a class="navbar-brand" href="{% url 'polls:index' %}">📊 Ankiety</a>
        <div class="navbar-nav ms-auto">
            {% if user.is_authenticated %}
                <span class="nav-item nav-link text-light">{{ user.username }}</span>
                <a class="nav-link text-light" href="{% url 'logout' %}">Wyloguj</a>
            {% else %}
                <a class="nav-link text-light" href="{% url 'login' %}">Zaloguj</a>
            {% endif %}
        </div>
    </div>
</nav>

<div class="container">
    {% block content %}{% endblock %}
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

---

### Krok 2: Zaktualizuj `index.html`

```html
{% extends 'polls/base.html' %}

{% block title %}Lista pytań{% endblock %}

{% block content %}
<h1 class="mb-4">Dostępne ankiety</h1>

{% if latest_question_list %}
    <div class="row">
    {% for question in latest_question_list %}
        <div class="col-md-6 mb-3">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">{{ question.question_text }}</h5>
                    <p class="card-text text-muted">
                        <small>Opublikowano: {{ question.pub_date|date:"d.m.Y" }}</small>
                    </p>
                    <a href="{% url 'polls:detail' question.id %}" class="btn btn-primary">Głosuj</a>
                    <a href="{% url 'polls:results' question.id %}" class="btn btn-outline-secondary">Wyniki</a>
                </div>
            </div>
        </div>
    {% endfor %}
    </div>
{% else %}
    <div class="alert alert-info">Brak dostępnych ankiet.</div>
{% endif %}
{% endblock %}
```

---

### Krok 3: Zaktualizuj `detail.html`

```html
{% extends 'polls/base.html' %}

{% block title %}{{ question.question_text }}{% endblock %}

{% block content %}
<h1 class="mb-4">{{ question.question_text }}</h1>

{% if error_message %}
    <div class="alert alert-danger">{{ error_message }}</div>
{% endif %}

<form action="{% url 'polls:vote' question.id %}" method="post">
{% csrf_token %}
<div class="list-group mb-3">
{% for choice in question.choice_set.all %}
    <label class="list-group-item list-group-item-action">
        <input type="radio" name="choice" value="{{ choice.id }}" class="me-2">
        {{ choice.choice_text }}
    </label>
{% endfor %}
</div>
<button type="submit" class="btn btn-success">Głosuj</button>
<a href="{% url 'polls:index' %}" class="btn btn-outline-secondary ms-2">Wróć</a>
</form>
{% endblock %}
```

---

### Krok 4: Zaktualizuj `results.html`

```html
{% extends 'polls/base.html' %}

{% block title %}Wyniki – {{ question.question_text }}{% endblock %}

{% block content %}
<h1 class="mb-4">Wyniki: {{ question.question_text }}</h1>

{% with total=question.choice_set.all|length %}
<ul class="list-group mb-4">
{% for choice in question.choice_set.all %}
    <li class="list-group-item d-flex justify-content-between align-items-center">
        {{ choice.choice_text }}
        <span class="badge bg-primary rounded-pill">{{ choice.votes }} głosów</span>
    </li>
{% endfor %}
</ul>
{% endwith %}

<a href="{% url 'polls:detail' question.id %}" class="btn btn-primary">Głosuj ponownie</a>
<a href="{% url 'polls:index' %}" class="btn btn-outline-secondary ms-2">Lista ankiet</a>
{% endblock %}
```

---

### Krok 5: Przetestuj

Uruchom serwer i sprawdź wygląd wszystkich stron w przeglądarce.

---

## Efekt końcowy

Po wykonaniu zadania aplikacja powinna wyglądać jak profesjonalna strona z:
- Responsywnym navbar
- Kartami z pytaniami (card grid)
- Stylowanym formularzem głosowania
- Tablicą wyników z badges
