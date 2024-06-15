---

# Aplikacja dla Korepetytorów

Aplikacja dla korepetytorów to zaawansowane narzędzie webowe stworzone w Django, które umożliwia zarządzanie interakcjami między nauczycielami, uczniami i rodzicami. Wykorzystuje SQLite jako bazy danych oraz Docker do łatwego wdrożenia i skalowania.

## Funkcje

### Dla Nauczyciela
- **Zarządzanie Lekcjami:** Planowanie i organizacja lekcji.
- **Zadania:** Dodawanie, usuwanie i ocenianie zadań przesłanych przez uczniów.
- **Forum:** Publikowanie ogłoszeń i postów na forum.
- **Monitorowanie Postępów:** Podgląd wykresów i postępów każdego ucznia.

### Dla Ucznia
- **Dostęp do Materiałów:** Przeglądanie postów i ogłoszeń nauczyciela.
- **Zadania:** Wysyłanie wykonanych zadań, edycja nieocenionych zadań.
- **Kalendarz:** Dostęp do kalendarza z planowanymi lekcjami i terminami zadań.
- **Analiza Postępów:** Wykresy ilustrujące własne postępy.

### Dla Rodzica
- **Przegląd Dzieci:** Lista dzieci uczęszczających na korepetycje.
- **Informacje o Płatnościach:** Szczegóły dotyczące opłat za lekcje.
- **Zarządzanie Lekcjami:** Możliwość odwołania lekcji na co najmniej 48 godzin przed jej rozpoczęciem.

## Wymagania Techniczne

- Python 3.9+
- Django 4.2.1+
- Docker & Docker Compose


## Zabezpieczenia

Django zapewnia wbudowaną ochronę przed atakami CSRF poprzez implementację tokenów CSRF w formularzach, co minimalizuje ryzyko ataków typu Cross-Site Request Forgery. Ponadto, framework chroni przed atakami XSS (Cross-Site Scripting) poprzez odpowiednie sanitowanie danych wprowadzanych przez użytkowników. Django ORM (Object-Relational Mapping) pomaga zminimalizować ryzyko SQL Injection, ponieważ korzysta z abstrakcyjnego API do baz danych, co zapobiega bezpośredniemu wstrzykiwaniu szkodliwego kodu SQL. Dodatkowo, hasła są bezpiecznie przechowywane, używając hashowania SHA256 oraz algorytmu PBKDF2 z solą, co jest zgodne z rekomendacjami NIST i OWASP

## Instalacja i Uruchomienie

Aby uruchomić aplikację:

1. Sklonuj repozytorium:

   ```
   git clone https://github.com/mvnuela/aplikacje-webowe.git
   cd aplikacje-webowe
   ```

2. Uruchom Docker Compose:

   ```
   docker-compose up --build
   ```

Aplikacja jest dostępna pod adresem `http://127.0.0.1:8000`.

### Panel Administratora

Po uruchomieniu, dostęp do panelu admina jest możliwy pod adresem `http://127.0.0.1:8000/admin`. Login: `admin1`, hasło: `aplikacjawebowa1`. 

