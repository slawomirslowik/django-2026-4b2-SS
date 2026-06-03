# Zadanie: Wykorzystanie AI w programowaniu Django

## Cel zadania

Poznaj darmowe narzędzia AI wspomagające programowanie i wykorzystaj je do rozbudowy aplikacji `polls` w Django – od generowania kodu, przez tworzenie szablonów HTML, aż po pisanie testów.

---

## Darmowe narzędzia AI do programowania

| Narzędzie | Typ | Link |
|---|---|---|
| **Blackbox AI** | Asystent w przeglądarce + wtyczka VS Code | https://www.blackbox.ai |
| **GitHub Copilot** | Wtyczka VS Code (darmowy dla studentów) | https://github.com/features/copilot |
| **Codeium** | Wtyczka VS Code – w pełni darmowy | https://codeium.com |
| **ChatGPT (GPT-4o mini)** | Chatbot w przeglądarce | https://chat.openai.com |
| **Google Gemini** | Chatbot w przeglądarce | https://gemini.google.com |
| **Cursor** | Edytor kodu z AI (darmowy plan) | https://www.cursor.com |

> **Rekomendacja:** Blackbox AI i Codeium są w pełni darmowe i działają bezpośrednio w VS Code jako wtyczki – bez konieczności rejestracji karty płatniczej.

---

## Przygotowanie

1. Zainstaluj wtyczkę **Blackbox AI** lub **Codeium** w VS Code.
2. Upewnij się, że aplikacja `polls` działa i masz uruchomiony serwer.

---

## Zadanie 1: Wygeneruj nowy widok za pomocą AI

Za pomocą wybranego narzędzia AI (Blackbox / Codeium / ChatGPT) wygeneruj widok, który wyświetli **statystyki głosowania** – liczbę oddanych głosów dla każdego pytania.

**Wskazówka – prompt do AI:**
```
Napisz widok Django (function-based view), który pobiera wszystkie pytania z modelu Question 
wraz z sumą głosów dla każdego pytania (przez powiązany model Choice) 
i przekazuje je do szablonu stats.html.
```

Następnie:
- Dodaj widok do `polls/views.py`
- Dodaj URL w `polls/urls.py` pod adresem `/polls/stats/`
- Stwórz szablon `polls/templates/polls/stats.html`

---

## Zadanie 2: Wygeneruj szablon HTML z pomocą AI

Poproś AI o wygenerowanie **ładnego szablonu HTML** dla strony głównej aplikacji polls (`index.html`), który zawiera:
- Tytuł strony
- Listę pytań jako karty (cards)
- Informację o liczbie odpowiedzi dla każdego pytania
- Link do głosowania

**Przykładowy prompt:**
```
Wygeneruj szablon HTML dla aplikacji ankietowej Django. 
Strona ma wyświetlać listę pytań (question_text) jako karty Bootstrap. 
Każda karta ma zawierać link do szczegółów pytania (polls:detail) 
i datę publikacji (pub_date). Użyj Bootstrap 5 z CDN.
```

Wygenerowany kod wklej do `polls/templates/polls/index.html`.

---

## Zadanie 3: Napisz testy z pomocą AI

Za pomocą AI wygeneruj testy jednostkowe dla nowego widoku statystyk.

**Przykładowy prompt:**
```
Napisz testy Django (TestCase) dla widoku stats w aplikacji polls.
Widok jest dostępny pod adresem 'polls:stats'.
Przetestuj: kod odpowiedzi 200, obecność pytania w kontekście, 
brak pytań oraz wyświetlanie pytań z przeszłości i przyszłości.
```

Wygenerowane testy dodaj do `polls/tests.py` i uruchom:
```
py manage.py test polls
```

---

## Zadanie 4: Popraw i zrefaktoryzuj kod z AI

Wklej do Blackbox AI / ChatGPT swój aktualny plik `polls/views.py` i poproś o:
- Dodanie komentarzy/docstringów
- Uproszczenie zapytań do bazy danych
- Zaproponowanie użycia widoków generycznych tam, gdzie jeszcze ich nie ma

**Prompt:**
```
Przejrzyj poniższy kod widoków Django i zaproponuj ulepszenia: 
dodaj docstringi, uprość zapytania ORM, użyj widoków generycznych gdzie to możliwe.
[wklej kod]
```

---

## Zadanie 5 (dodatkowe): Wygeneruj model z pomocą AI

Poproś AI o zaprojektowanie nowego modelu `Tag`, który pozwoli przypisywać tagi do pytań (relacja wiele do wielu).

**Prompt:**
```
Zaprojektuj model Django Tag z polami: name (CharField) i slug (SlugField).
Dodaj relację ManyToMany między Tag a Question w aplikacji polls.
Napisz też metodę __str__ dla modelu Tag.
```

Po wygenerowaniu:
- Dodaj model do `polls/models.py`
- Utwórz i zastosuj migracje

---

## Ocena zadania

| Kryterium | Punkty |
|---|---|
| Działający widok statystyk | 2 |
| Poprawny szablon HTML z Bootstrap | 2 |
| Testy widoku statystyk | 2 |
| Refaktoryzacja views.py | 2 |
| Zadanie dodatkowe (model Tag) | 2 |
| **Razem** | **10** |

---

## Wskazówki

- Nie kopiuj kodu AI ślepo – zawsze przeczytaj, zrozum i ewentualnie popraw wygenerowany kod.
- AI często generuje kod dla starszych wersji Django – sprawdź czy składnia jest zgodna z Django 5/6.
- Blackbox AI ma funkcję **"Explain Code"** – możesz zaznaczyć fragment kodu i poprosić o wyjaśnienie.
- Jeśli AI wygeneruje błędny kod, opisz błąd i poproś o poprawkę w tym samym czacie.
