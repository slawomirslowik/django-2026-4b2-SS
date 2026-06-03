# Zadanie 9: Prosty REST API endpoint

## Cel
Stwórz endpoint `/polls/api/questions/` zwracający listę pytań w formacie JSON. Opcjonalnie użyj Django REST Framework.

---

## Wariant A: Bez dodatkowych bibliotek (JsonResponse)

### Krok 1: Dodaj widok API

Otwórz `polls/views.py` i dodaj:

```python
from django.http import JsonResponse

def api_questions(request):
    questions = Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')

    data = [
        {
            'id': q.id,
            'question_text': q.question_text,
            'pub_date': q.pub_date.isoformat(),
            'choices': [
                {'id': c.id, 'choice_text': c.choice_text, 'votes': c.votes}
                for c in q.choice_set.all()
            ]
        }
        for q in questions
    ]
    return JsonResponse({'questions': data})
```

### Krok 2: Dodaj URL

```python
path('api/questions/', views.api_questions, name='api_questions'),
```

### Krok 3: Przetestuj

Wejdź na `http://127.0.0.1:8000/polls/api/questions/` – przeglądarka pokaże JSON.

---

## Wariant B: Z Django REST Framework (DRF)

### Krok 1: Zainstaluj DRF

```
pip install djangorestframework
```

Dodaj do `INSTALLED_APPS` w `settings.py`:

```python
'rest_framework',
```

### Krok 2: Utwórz serializery

Utwórz plik `polls/serializers.py`:

```python
from rest_framework import serializers
from .models import Question, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(source='choice_set', many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'choices']
```

### Krok 3: Utwórz widoki API

W `polls/views.py`:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import QuestionSerializer

@api_view(['GET'])
def api_questions_drf(request):
    questions = Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)
```

### Krok 4: Dodaj URL

```python
path('api/questions/', views.api_questions_drf, name='api_questions'),
```

### Krok 5: Przetestuj

Wejdź na `http://127.0.0.1:8000/polls/api/questions/` – DRF pokaże czytelny interfejs przeglądarkowy.

---

## Rozwiązanie – pełny kod (Wariant A)

### `polls/views.py`

```python
from django.http import JsonResponse
from django.utils import timezone
from .models import Question


def api_questions(request):
    questions = Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date').prefetch_related('choice_set')

    data = [
        {
            'id': q.id,
            'question_text': q.question_text,
            'pub_date': q.pub_date.isoformat(),
            'category': q.category.name if q.category else None,
            'choices': [
                {
                    'id': c.id,
                    'choice_text': c.choice_text,
                    'votes': c.votes
                }
                for c in q.choice_set.all()
            ]
        }
        for q in questions
    ]
    return JsonResponse({'questions': data})
```
