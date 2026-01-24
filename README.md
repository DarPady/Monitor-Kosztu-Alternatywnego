# Monitor Kosztu Alternatywnego (MKA)

 ## Spis treści
- [Charakterystyka oprogramowania](#charakterystyka-oprogramowania)
- [Prawa  autorskie](#Prawa-autorskie)
- [Specyfikacja wymagań](#specyfikacja-wymagań)
- [Architektura systemu/oprogramowania](#architektura-systemu/oprogramowania)
- [Instalacja](#instalacja)
- [Testy](#testy)



---

## Charakterystyka oprogramowania
Projekt nosi nazwę MKA - Monitor Kosztu Alternatywnego

Celem projektu jest analiza kosztu alternatywnego w kontekście osobistych finansów i ekonomii behawioralnej, ilościowo przedstawiając realne skutki utrwalonych, drobnych nawyków konsumpcyjnych, takich jak codzienne wydatki na używki czy inne przyjemności.

Produktem końcowym jest interaktywna aplikacja webowa, posiadająca funkcję śledzenia nawyków oraz przeliczaniem codziennych wydatków na aktualną wartość potencjalnych inwestycji. Celem projektu jest nie tylko edukacja użytkowników w zakresie finansów osobistych i zarządzania własnym budżetem, ale także pokazanie realnego wpływu codziennych wydatków na długoterminowy potencjał inwestycyjny.


---
## Prawa  autorskie

### Licencja

Projekt udostępniamy na licencji **MIT**.

Licencja MIT jest jedną z najprostszych i najbardziej liberalnych licencji otwartego oprogramowania. Oznacza to, że dozwolone jest:
* korzystanie z projektu prywatnie i komercyjnie,
* kopiowanie i rozpowszechnianie kodu,
* modyfikowanie go i tworzenie na jego bazie własne rozwiązania,
* publikowanie własnych wersji i łączenie tego kodu z innym oprogramowaniem.

Jedyny kluczowy wymóg to zachowanie informacji o prawach autorskich i licencji w kopiach lub istotnych częściach oprogramowania.
Projekt jest dostarczany „as is”. Autorzy nie ponoszą odpowiedzialności za szkody wynikłe z używania oprogramowania.

Wybrałyśmy licencję MIT, ponieważ chcemy, żeby z projektu dało się łatwo korzystać w pracach badawczych, innych projektach czy nawet komercyjnie.  Nie zależy nam na stawianiu dodatkowych barier: jeśli ktoś chce utworzyć fork, coś poprawić albo rozwinąć kod, ma do tego pełne przyzwolenie.

Treść licencji: https://opensource.org/license/mit/


### Autorzy
Jeśli masz jakieś pytania lub sugestie, skontaktuj się z nami:

**Profil  GitHub**:
* Daria Padytel - [DarPady](https://github.com/DarPady)
* Julia Rutkowska - [rutkowskaj](https://github.com/rutkowskaj)
* Katarzyna Zaniewska - [KatarzynaZaniewska](https://github.com/KatarzynaZaniewska)

---

## Specyfikacja wymagań

### Wymagania funkcjonalne

**MODUŁ 1: KONFIGURACJA NAWYKÓW**
| ID | NAZWA | OPIS | PRIORYTET | 
|----|-------|------|-----------|
|F-01|Definicja śledzonego produktu| Użytkownik musi mieć możliwość zdefiniowania nowego produktu/nawyku poprzez podanie: nazwy (np. "Papierosy"), jednostki miary (np. "paczka") oraz ceny jednostkowej.|1|
|F-02|Edycja ceny produktu| Użytkownik musi mieć możliwość aktualizacji ceny produktu. System musi zachować historię cen, aby stare wpisy były przeliczane po starej cenie, a nowe po nowej.|1|
|F-03|Zarządzanie listą produktów| Użytkownik może dodawać wiele niezależnych produktów (np. "Kawa", "Papierosy") i śledzić je równolegle.|1|
|F-04|Edycja parametrów historycznych| Możliwość wpisania, jak długo użytkownik już posiada dany nawyk, aby obliczyć stratę "wsteczną".|3|

**MODUŁ 2: DZIENNIK KONSUMPCJI**
| ID | NAZWA | OPIS | PRIORYTET | 
|----|-------|------|-----------|
|F-05|Rejestracja zużycia| System musi umożliwiać użytkownikowi codzienne wprowadzenie ilości zużytego produktu (np. 1.5 sztuki) dla wybranej daty.|1|
|F-06|Automatyczne obliczanie kosztu| Natychmiast po wprowadzeniu ilości, system musi obliczyć dzienny koszt (ilość × aktualna cena) i zapisać go w bazie danych.|1|

**MODUŁ 3: POZYSKANIE DANYCH RYNKOWYCH**
| ID | NAZWA | OPIS | PRIORYTET | 
|----|-------|------|-----------|
|F-07|Połączenie z Bankier.pl| System musi cyklicznie łączyć się ze stroną Bankier.pl, imitując przeglądarkę, aby uniknąć blokady i pobrać pełny kod źródłowy HTML.|1|
|F-08|Ekstrakcja notowań indeksu| System musi wyszukać w pobranym kodzie HTML aktualną wartość wybranego notowania giełdowego, wraz ze zmianą procentową i pobrać te wartości wraz z timestampem. |1|
|F-09|Czyszczenie i konwersja danych| System musi oczyścić pobrane z HTML dane (usunięcie spacji, zamiana przecinków na kropki) i przekonwertować je na format liczbowy. |1|
|F-10|Cykliczna aktualizacja| Proces scrapingu musi być uruchamiany automatycznie o godz. 12.00 lub po interakcji dowolnego użytkownika.|1|

**MODUŁ 4: ANALIZA DANYCH**
| ID | NAZWA | OPIS | PRIORYTET | 
|----|-------|------|-----------|
|F-11|Obliczanie sumy wydatków| System musi agregować dane o wydatkach w danym dniu i łączną ich sumę.|1|
|F-12|Symulacja inwestycyjna| System sprawdza, ile dziś byłyby warte wydane pieniądze, gdyby były na bieżąco inwestowane w wybrane walory.|1|
|F-13|Konfiguracja portfela| System umożliwia ustalenie wag dla każdego z sześciu walorów, jednocześnie sprawdzając czy suma wynosi 100%.|2|
|F-14|Wykres inwestycyjny| Wyświetlana jest zmiana wartości portfela w czasie.|3|

**MODUŁ 6: PROFIL UŻYTKOWNIKA**
| ID | NAZWA | OPIS | PRIORYTET | 
|----|-------|------|-----------|
|F-15|Rejestracja i logowanie| Po utworzeniu konta system zapisuje wprowadzone przez użytkownika dane i przypisuje je do jego profilu.|1|

### Wymagania niefunkcjonalne

| ID | NAZWA | OPIS | PRIORYTET | 
|----|-------|------|-----------|
|NF-01|Dostęp do aplikacji| System musi być dostępny przez przeglądarkę internetową (aplikacja webowa) i nie wymagać instalacji.|1|
|NF-02|Interfejs użytkownika| System nie wymaga obsługi przez wiersz poleceń; wszystkie funkcje dostępne dla użytkownika są dostępne przez GUI.|1|
|NF-03|Dane historyczne| Dane użytkowników i historia notowań muszą być przechowywane w bazie danych.|1|

(Priorytet: 1 - wymagane, 2 - przydatne, 3 - opcjonalne)

---

## Architektura systemu/oprogramowania

Architektura rozwoju

| Technologia | Przeznaczenie | Nr wersji |
|----|-------|------|
|Python|Język programowania|3.13.11|
|GitHub|Hosting repozytorium|-|
|Git|Kontrola wersji|2.52|
|Biblioteka "beautifulsoup4"|Parsowanie dokumentów HTML/XML|4.14.3|
|Biblioteka "Flask"|Tworzy aplikacje internetową i obsługuje żądań HTTP.|3.1.2|
|Biblioteka "Flask-Login"|Obsługa logowania|0.6.3|
|Biblioteka "Flask-SQLAlchemy"|Obsługa bazy danych|3.1.1|
|Biblioteka "requests"|Zapytania HTTP|2.32.5|

    
---

## Instalacja

### Wymagania wstępne
1. Python 3.x (rekomendowane 3.11+)
2. Narzędzie do tworzenia środowisk wirtualnych (np. venv lub virtualenv)
3. Dostęp do internetu (pobieranie notowań z Bankier.pl)


### Procedura instalacji
1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/DarPady/Monitor-Kosztu-Alternatywnego.git
   cd Monitor-Kosztu-Alternatywnego/Project
   ```

2. Utwórz i aktywuj środowisko wirtualne:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Zainstaluj wymagane zależności Pythona:
   ```bash
   pip install -r requirements.txt
   ```

4. Uruchom serwer deweloperski:
   ```bash
   python app.py
   ```

5. Otwórz aplikację w przeglądarce:
   ```
   http://127.0.0.1:5000
   ```
---

## Testy
W projekcie przeprowadzono **testy akceptacyjne (manualne)**, które obejmowały:
- rejestrację i logowanie użytkownika,
- konfigurację nawyków/produktów (dodawanie wielu produktów, zmiana ceny z zachowaniem historii),
- rejestrację dziennego zużycia oraz automatyczne wyliczanie kosztu,
- pobieranie danych rynkowych (scraping), ich przetwarzanie i cykliczną aktualizację,
- agregację wydatków oraz symulację inwestycyjną,
- wymagania niefunkcjonalne: dostęp przez przeglądarkę, obsługa przez GUI oraz trwałe przechowywanie danych w bazie.

Szczegółowe scenariusze i raport z testów: [Testy_akceptacyjne](Testy_akceptacyjne.pdf)

---
