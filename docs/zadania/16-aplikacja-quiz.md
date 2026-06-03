# Zadanie 16: Własna aplikacja ankietowa – Quiz

## Cel
Stwórz nową aplikację `quiz` wzorowaną na `polls`, ale z własną logiką: pytania mają jedną poprawną odpowiedź, a użytkownik dostaje wynik punktowy po zakończeniu quizu.

---

## Instrukcja krok po kroku

### Krok 1: Utwórz aplikację `quiz`

```
py manage.py startapp quiz
```

Dodaj do `INSTALLED_APPS` w `settings.py`:

```python
'quiz',
```

---

### Krok 2: Zaprojektuj modele

Utwórz `quiz/models.py`:

```python
from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=500)

    def __str__(self):
        return self.question_text


class QuizAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.answer_text} ({'✓' if self.is_correct else '✗'})"
```

---

### Krok 3: Utwórz i zastosuj migracje

```
py manage.py makemigrations quiz
py manage.py migrate
```

---

### Krok 4: Zarejestruj modele w admin

Utwórz `quiz/admin.py`:

```python
from django.contrib import admin
from .models import Quiz, QuizQuestion, QuizAnswer


class QuizAnswerInline(admin.TabularInline):
    model = QuizAnswer
    extra = 4


class QuizQuestionInline(admin.StackedInline):
    model = QuizQuestion
    extra = 2


class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    inlines = [QuizQuestionInline]


class QuizQuestionAdmin(admin.ModelAdmin):
    inlines = [QuizAnswerInline]


admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizQuestion, QuizQuestionAdmin)
```

---

### Krok 5: Stwórz widoki

Utwórz `quiz/views.py`:

```python
from django.shortcuts import get_object_or_404, render, redirect
from .models import Quiz, QuizQuestion, QuizAnswer


def quiz_list(request):
    quizzes = Quiz.objects.all().order_by('-created_at')
    return render(request, 'quiz/list.html', {'quizzes': quizzes})


def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.prefetch_related('answers').all()
    return render(request, 'quiz/detail.html', {
        'quiz': quiz,
        'questions': questions
    })


def quiz_submit(request, quiz_id):
    if request.method != 'POST':
        return redirect('quiz:detail', quiz_id=quiz_id)

    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.prefetch_related('answers').all()

    score = 0
    results = []

    for question in questions:
        selected_id = request.POST.get(f'question_{question.id}')
        correct_answer = question.answers.filter(is_correct=True).first()

        is_correct = False
        selected_answer = None

        if selected_id:
            try:
                selected_answer = question.answers.get(pk=selected_id)
                is_correct = selected_answer.is_correct
                if is_correct:
                    score += 1
            except QuizAnswer.DoesNotExist:
                pass

        results.append({
            'question': question,
            'selected': selected_answer,
            'correct': correct_answer,
            'is_correct': is_correct,
        })

    total = questions.count()
    percentage = round(score / total * 100) if total > 0 else 0

    return render(request, 'quiz/result.html', {
        'quiz': quiz,
        'score': score,
        'total': total,
        'percentage': percentage,
        'results': results,
    })
```

---

### Krok 6: Skonfiguruj URL

Utwórz `quiz/urls.py`:

```python
from django.urls import path
from . import views

app_name = 'quiz'
urlpatterns = [
    path('', views.quiz_list, name='list'),
    path('<int:quiz_id>/', views.quiz_detail, name='detail'),
    path('<int:quiz_id>/submit/', views.quiz_submit, name='submit'),
]
```

Dodaj do `mysite/urls.py`:

```python
path('quiz/', include('quiz.urls')),
```

---

### Krok 7: Utwórz szablony

**`quiz/templates/quiz/list.html`:**

```html
<h1>Dostępne quizy</h1>
<ul>
{% for quiz in quizzes %}
    <li>
        <a href="{% url 'quiz:detail' quiz.id %}">{{ quiz.title }}</a>
        <small>{{ quiz.description }}</small>
    </li>
{% empty %}
    <li>Brak dostępnych quizów.</li>
{% endfor %}
</ul>
```

**`quiz/templates/quiz/detail.html`:**

```html
<h1>{{ quiz.title }}</h1>
<p>{{ quiz.description }}</p>

<form action="{% url 'quiz:submit' quiz.id %}" method="post">
{% csrf_token %}
{% for question in questions %}
    <div>
        <h3>{{ forloop.counter }}. {{ question.question_text }}</h3>
        {% for answer in question.answers.all %}
            <label>
                <input type="radio" name="question_{{ question.id }}" value="{{ answer.id }}">
                {{ answer.answer_text }}
            </label><br>
        {% endfor %}
    </div>
{% endfor %}
<button type="submit">Sprawdź odpowiedzi</button>
</form>
```

**`quiz/templates/quiz/result.html`:**

```html
<h1>Wynik: {{ score }} / {{ total }} ({{ percentage }}%)</h1>

{% if percentage >= 80 %}
    <p>🎉 Świetny wynik!</p>
{% elif percentage >= 50 %}
    <p>👍 Dobry wynik!</p>
{% else %}
    <p>📚 Warto powtórzyć materiał.</p>
{% endif %}

<h2>Szczegóły odpowiedzi:</h2>
{% for result in results %}
    <div>
        <strong>{{ forloop.counter }}. {{ result.question.question_text }}</strong><br>
        Twoja odpowiedź: {{ result.selected.answer_text|default:"Nie wybrano" }}
        {% if result.is_correct %}✅{% else %}❌{% endif %}<br>
        {% if not result.is_correct %}
            Poprawna odpowiedź: {{ result.correct.answer_text }}
        {% endif %}
    </div>
{% endfor %}

<a href="{% url 'quiz:detail' quiz.id %}">Spróbuj ponownie</a>
<a href="{% url 'quiz:list' %}">Lista quizów</a>
```

---

### Krok 8: Przetestuj

1. Dodaj quiz z pytaniami przez panel admina
2. Wejdź na `http://127.0.0.1:8000/quiz/`
3. Rozwiąż quiz i sprawdź wyniki
