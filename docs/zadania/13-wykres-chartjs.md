# Zadanie 13: Wykres wyników głosowania z Chart.js

## Cel
Wyświetl wyniki głosowania jako wykres słupkowy lub kołowy używając biblioteki Chart.js (ładowanej z CDN).

---

## Instrukcja krok po kroku

### Krok 1: Zaktualizuj widok `results`

Widok nie wymaga zmian – `DetailView` przekazuje obiekt `question` do szablonu. Dane do wykresu wygenerujemy bezpośrednio w szablonie.

---

### Krok 2: Zaktualizuj szablon `results.html`

Dodaj element `<canvas>` dla wykresu i skrypt Chart.js:

```html
<h1>{{ question.question_text }}</h1>

<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} — {{ choice.votes }} głosów</li>
{% endfor %}
</ul>

<!-- Wykres -->
<div style="max-width: 600px; margin-top: 30px;">
    <canvas id="resultsChart"></canvas>
</div>

<a href="{% url 'polls:detail' question.id %}">Głosuj ponownie</a>
<a href="{% url 'polls:index' %}">Lista ankiet</a>

<!-- Chart.js z CDN -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    // Dane z Django (przekazane przez szablon)
    const labels = [{% for choice in question.choice_set.all %}'{{ choice.choice_text|escapejs }}',{% endfor %}];
    const data = [{% for choice in question.choice_set.all %}{{ choice.votes }},{% endfor %}];
    const backgroundColors = [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
        '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
    ];

    const ctx = document.getElementById('resultsChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',  // zmień na 'pie' lub 'doughnut' dla wykresu kołowego
        data: {
            labels: labels,
            datasets: [{
                label: 'Liczba głosów',
                data: data,
                backgroundColor: backgroundColors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                title: {
                    display: true,
                    text: 'Wyniki głosowania'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { stepSize: 1 }
                }
            }
        }
    });
</script>
```

---

### Krok 3: Dodaj wybór typu wykresu (opcjonalnie)

Dodaj przyciski przełączające między typami wykresów:

```html
<div>
    <button onclick="changeChart('bar')">Słupkowy</button>
    <button onclick="changeChart('pie')">Kołowy</button>
    <button onclick="changeChart('doughnut')">Pierścieniowy</button>
</div>

<script>
let chart;

function createChart(type) {
    if (chart) chart.destroy();
    const ctx = document.getElementById('resultsChart').getContext('2d');
    chart = new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: 'Głosy',
                data: data,
                backgroundColor: backgroundColors,
            }]
        },
        options: { responsive: true }
    });
}

function changeChart(type) {
    createChart(type);
}

createChart('bar');
</script>
```

---

### Krok 4: Przetestuj

1. Zagłosuj kilka razy na różne odpowiedzi
2. Wejdź na `/polls/<id>/results/`
3. Sprawdź czy wykres wyświetla się poprawnie

---

## Rozwiązanie – pełny `results.html`

```html
{% extends 'polls/base.html' %}

{% block title %}Wyniki – {{ question.question_text }}{% endblock %}

{% block content %}
<h1 class="mb-4">{{ question.question_text }}</h1>

<ul class="list-group mb-4">
{% for choice in question.choice_set.all %}
    <li class="list-group-item d-flex justify-content-between">
        {{ choice.choice_text }}
        <span class="badge bg-primary">{{ choice.votes }} głosów</span>
    </li>
{% endfor %}
</ul>

<div class="mb-3">
    <button class="btn btn-sm btn-outline-primary" onclick="changeChart('bar')">Słupkowy</button>
    <button class="btn btn-sm btn-outline-primary" onclick="changeChart('pie')">Kołowy</button>
    <button class="btn btn-sm btn-outline-primary" onclick="changeChart('doughnut')">Pierścieniowy</button>
</div>

<div style="max-width: 500px;">
    <canvas id="resultsChart"></canvas>
</div>

<div class="mt-4">
    <a href="{% url 'polls:detail' question.id %}" class="btn btn-primary">Głosuj ponownie</a>
    <a href="{% url 'polls:index' %}" class="btn btn-outline-secondary ms-2">Lista ankiet</a>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const labels = [{% for choice in question.choice_set.all %}'{{ choice.choice_text|escapejs }}',{% endfor %}];
const votes = [{% for choice in question.choice_set.all %}{{ choice.votes }},{% endfor %}];
const colors = ['#FF6384','#36A2EB','#FFCE56','#4BC0C0','#9966FF','#FF9F40'];

let chart;

function changeChart(type) {
    if (chart) chart.destroy();
    chart = new Chart(document.getElementById('resultsChart'), {
        type: type,
        data: {
            labels: labels,
            datasets: [{ data: votes, backgroundColor: colors, label: 'Głosy' }]
        },
        options: {
            responsive: true,
            plugins: { title: { display: true, text: 'Wyniki głosowania' } },
            scales: type === 'bar' ? { y: { beginAtZero: true, ticks: { stepSize: 1 } } } : {}
        }
    });
}
changeChart('bar');
</script>
{% endblock %}
```
