# 📚 Projekt: Rozbudowa aplikacji Polls – Przewodnik zadań

## Opis projektu

Celem projektu jest samodzielna rozbudowa aplikacji ankietowej `polls` stworzonej w ramach kursu Django. Każde zadanie jest niezależne i można je realizować w dowolnej kolejności. Zadania są podzielone na trzy poziomy trudności i oceniane w skali **1–10 punktów**.

Szczegółowe instrukcje i rozwiązania do każdego zadania znajdują się w katalogu `docs/zadania/`.

---

## 🟢 Poziom podstawowy (1–3 pkt)

Zadania odpowiednie dla osób zaczynających pracę z Django. Wymagają znajomości modeli, widoków i szablonów na poziomie tutoriala.

| # | Zadanie | Opis | Plik z instrukcją | Punkty |
|---|---|---|---|:---:|
| 1 | **Panel admina** | Rejestracja modeli `Question`, `Choice`, `Category` w panelu admina z customizacją: kolumny, wyszukiwarka, filtry, inline dla odpowiedzi | `01-panel-admina.md` | 2 |
| 2 | **Stronicowanie** | Ograniczenie listy pytań do 5 na stronę z nawigacją (Django Paginator) | `02-stronicowanie.md` | 2 |
| 3 | **Licznik głosów** | Wyświetlenie łącznej liczby głosów przy każdym pytaniu na liście (Django ORM `annotate`) | `03-licznik-glosow.md` | 3 |
| 4 | **Ochrona przed wielokrotnym głosowaniem** | Zabezpieczenie widoku `vote` sesjami Django – użytkownik może głosować tylko raz | `04-ochrona-przed-wielokrotnym-glosowaniem.md` | 3 |

---

## 🟡 Poziom średni (4–6 pkt)

Zadania wymagające samodzielnego projektowania logiki aplikacji, nowych widoków i rozszerzeń ORM.

| # | Zadanie | Opis | Plik z instrukcją | Punkty |
|---|---|---|---|:---:|
| 5 | **Wyszukiwarka pytań** | Formularz GET + obiekt `Q` do wyszukiwania pytań po tekście | `05-wyszukiwarka.md` | 4 |
| 6 | **Filtrowanie po kategorii** | Lista pytań filtrowana po modelu `Category` przez parametr w URL | `06-filtrowanie-po-kategorii.md` | 4 |
| 7 | **Sortowanie pytań** | Możliwość sortowania listy po dacie lub liczbie głosów (`?sort=date/votes`) | `07-sortowanie.md` | 4 |
| 8 | **Eksport wyników do CSV** | Widok pobierający wyniki głosowania jako plik `.csv` (z obsługą polskich znaków w Excelu) | `08-eksport-csv.md` | 5 |
| 9 | **REST API** | Endpoint `/polls/api/questions/` zwracający dane w JSON (`JsonResponse` lub Django REST Framework) | `09-rest-api.md` | 6 |
| 10 | **Autentykacja** | Zabezpieczenie widoku `vote` dekoratorem `@login_required`, strony logowania i wylogowania | `10-autentykacja.md` | 5 |

---

## 🔴 Poziom zaawansowany (7–10 pkt)

Zadania wymagające znajomości JavaScript, zewnętrznych bibliotek, architektury aplikacji lub konfiguracji środowiska produkcyjnego.

| # | Zadanie | Opis | Plik z instrukcją | Punkty |
|---|---|---|---|:---:|
| 11 | **Stylowanie Bootstrap 5** | Przeprojektowanie front-endu aplikacji z użyciem Bootstrap 5: navbar, karty, formularze, badges | `11-bootstrap.md` | 7 |
| 12 | **AJAX – głosowanie bez przeładowania** | Przebudowa formularza głosowania na Fetch API + JSON response, aktualizacja wyników w locie | `12-ajax-glosowanie.md` | 8 |
| 13 | **Wykres wyników (Chart.js)** | Wizualizacja wyników głosowania jako wykresy słupkowe, kołowe i pierścieniowe z przełącznikiem | `13-wykres-chartjs.md` | 7 |
| 14 | **Powiadomienia e-mail** | Wysyłanie e-maila do admina po przekroczeniu progu głosów; konfiguracja SMTP i zmiennych środowiskowych | `14-powiadomienia-email.md` | 7 |
| 15 | **Deployment na Railway/Render** | Wdrożenie projektu na darmowej platformie chmurowej: gunicorn, WhiteNoise, PostgreSQL, zmienne środowiskowe | `15-deployment.md` | 9 |
| 16 | **Własna aplikacja Quiz** | Nowa aplikacja `quiz` z własnym modelem pytań, jedną poprawną odpowiedzią i systemem punktacji | `16-aplikacja-quiz.md` | 8 |
| 17 | **Dashboard statystyk** | Osobna strona z podsumowaniem: łączne głosy, top-5 pytań, ankiety bez głosów, ostatnio dodane | `17-dashboard-statystyk.md` | 7 |
| 18 | **Wielojęzyczność (i18n)** | Obsługa tłumaczeń PL/EN, `gettext_lazy`, tagi `{% trans %}`, przełącznik języka | `18-wielojezycznosc.md` | 10 |

---

## 🤖 Zadanie z AI (bonus)

| # | Zadanie | Opis | Plik z instrukcją | Punkty |
|---|---|---|---|:---:|
| AI | **Programowanie z AI** | Wykorzystanie darmowych narzędzi AI (Blackbox, Codeium, ChatGPT) do generowania widoków, szablonów, testów i refaktoryzacji kodu | `../9-AI-w-programowaniu-django.md` | 5 |

---

## 📊 Podsumowanie punktacji

| Poziom | Liczba zadań | Punkty |
|---|:---:|:---:|
| 🟢 Podstawowy | 4 | 10 |
| 🟡 Średni | 6 | 28 |
| 🔴 Zaawansowany | 8 | 63 |
| 🤖 AI (bonus) | 1 | 5 |
| **Razem** | **19** | **106** |

---

## 📝 Zasady realizacji

1. Każde zadanie należy wykonać w osobnym branchu git: `git checkout -b zadanie-XX`
2. Po ukończeniu zadania utwórz pull request do brancha `main`
3. Kod musi działać poprawnie – uruchomiony serwer nie może zwracać błędów 500
4. Zadania z poziomów 🟡 i 🔴 wymagają co najmniej podstawowego testu działania
5. Można realizować zadania w dowolnej kolejności i łączyć ze sobą (np. Bootstrap + Chart.js + AJAX)

---

## 🔧 Wymagania wstępne

- Działająca aplikacja `polls` z modelem `Question`, `Choice`, `Category`
- Python 3.10+ i Django 5/6
- Wirtualne środowisko aktywowane
- Konto superusera (`py manage.py createsuperuser`)
