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

**1. MODUŁ 1: KONFIGURACJA NAWYKÓW (UŻYTKOWNIK)**
|ID | NAZWA | OPIS | PRIORYTET | 
|---|-------|------|-----------|
|F-01|Definicja śledzonego produktu| Użytkownik musi mieć możliwość zdefiniowania nowego produktu/nawyku poprzez podanie: nazwy (np. "Papierosy"), jednostki miary (np. "paczka") oraz ceny jednostkowej.|1|
|F-02|Edycja ceny produktu| Użytkownik musi mieć możliwość aktualizacji ceny produktu. System musi zachować historię cen, aby stare wpisy były przeliczane po starej cenie, a nowe po nowej.|1|
|F-03|Zarządzanie listą produktów| Użytkownik może dodawać wiele niezależnych produktów (np. "Kawa", "Papierosy") i śledzić je równolegle.|2|
|F-04|Edycja parametrów historycznych| Możliwość wpisania, jak długo użytkownik już posiada dany nawyk, aby obliczyć stratę "wsteczną".|3|

**2. MODUŁ 2: KONFIGURACJA NAWYKÓW (UŻYTKOWNIK)**
|ID | NAZWA | OPIS | PRIORYTET | 
|---|-------|------|-----------|
|F-01|Definicja śledzonego produktu| Użytkownik musi mieć możliwość zdefiniowania nowego produktu/nawyku poprzez podanie: nazwy (np. "Papierosy"), jednostki miary (np. "paczka") oraz ceny jednostkowej.|1|
|F-02|Edycja ceny produktu| Użytkownik musi mieć możliwość aktualizacji ceny produktu. System musi zachować historię cen, aby stare wpisy były przeliczane po starej cenie, a nowe po nowej.|1|
|F-03|Zarządzanie listą produktów| Użytkownik może dodawać wiele niezależnych produktów (np. "Kawa", "Papierosy") i śledzić je równolegle.|2|
|F-04|Edycja parametrów historycznych| Możliwość wpisania, jak długo użytkownik już posiada dany nawyk, aby obliczyć stratę "wsteczną".|3|

**3. MODUŁ 3: KONFIGURACJA NAWYKÓW (UŻYTKOWNIK)**
|ID | NAZWA | OPIS | PRIORYTET | 
|---|-------|------|-----------|
|F-01|Definicja śledzonego produktu| Użytkownik musi mieć możliwość zdefiniowania nowego produktu/nawyku poprzez podanie: nazwy (np. "Papierosy"), jednostki miary (np. "paczka") oraz ceny jednostkowej.|1|
|F-02|Edycja ceny produktu| Użytkownik musi mieć możliwość aktualizacji ceny produktu. System musi zachować historię cen, aby stare wpisy były przeliczane po starej cenie, a nowe po nowej.|1|
|F-03|Zarządzanie listą produktów| Użytkownik może dodawać wiele niezależnych produktów (np. "Kawa", "Papierosy") i śledzić je równolegle.|2|
|F-04|Edycja parametrów historycznych| Możliwość wpisania, jak długo użytkownik już posiada dany nawyk, aby obliczyć stratę "wsteczną".|3|

**4. MODUŁ 4: KONFIGURACJA NAWYKÓW (UŻYTKOWNIK)**
|ID | NAZWA | OPIS | PRIORYTET | 
|---|-------|------|-----------|
|F-01|Definicja śledzonego produktu| Użytkownik musi mieć możliwość zdefiniowania nowego produktu/nawyku poprzez podanie: nazwy (np. "Papierosy"), jednostki miary (np. "paczka") oraz ceny jednostkowej.|1|
|F-02|Edycja ceny produktu| Użytkownik musi mieć możliwość aktualizacji ceny produktu. System musi zachować historię cen, aby stare wpisy były przeliczane po starej cenie, a nowe po nowej.|1|
|F-03|Zarządzanie listą produktów| Użytkownik może dodawać wiele niezależnych produktów (np. "Kawa", "Papierosy") i śledzić je równolegle.|2|
|F-04|Edycja parametrów historycznych| Możliwość wpisania, jak długo użytkownik już posiada dany nawyk, aby obliczyć stratę "wsteczną".|3|

**5. MODUŁ 5: KONFIGURACJA NAWYKÓW (UŻYTKOWNIK)**
|ID | NAZWA | OPIS | PRIORYTET | 
|---|-------|------|-----------|
|F-01|Definicja śledzonego produktu| Użytkownik musi mieć możliwość zdefiniowania nowego produktu/nawyku poprzez podanie: nazwy (np. "Papierosy"), jednostki miary (np. "paczka") oraz ceny jednostkowej.|1|
|F-02|Edycja ceny produktu| Użytkownik musi mieć możliwość aktualizacji ceny produktu. System musi zachować historię cen, aby stare wpisy były przeliczane po starej cenie, a nowe po nowej.|1|
|F-03|Zarządzanie listą produktów| Użytkownik może dodawać wiele niezależnych produktów (np. "Kawa", "Papierosy") i śledzić je równolegle.|2|
|F-04|Edycja parametrów historycznych| Możliwość wpisania, jak długo użytkownik już posiada dany nawyk, aby obliczyć stratę "wsteczną".|3|

**6. MODUŁ 6: ZARZĄDZANIE UŻYTKOWNIKIEM**
|ID | NAZWA | OPIS | PRIORYTET | 
|---|-------|------|-----------|
|F-01|Definicja śledzonego produktu| Użytkownik musi mieć możliwość zdefiniowania nowego produktu/nawyku poprzez podanie: nazwy (np. "Papierosy"), jednostki miary (np. "paczka") oraz ceny jednostkowej.|1|
|F-02|Edycja ceny produktu| Użytkownik musi mieć możliwość aktualizacji ceny produktu. System musi zachować historię cen, aby stare wpisy były przeliczane po starej cenie, a nowe po nowej.|1|
|F-03|Zarządzanie listą produktów| Użytkownik może dodawać wiele niezależnych produktów (np. "Kawa", "Papierosy") i śledzić je równolegle.|2|
|F-04|Edycja parametrów historycznych| Możliwość wpisania, jak długo użytkownik już posiada dany nawyk, aby obliczyć stratę "wsteczną".|3|

### Wymagania niefunkcjonalne

|ID | NAZWA | OPIS | PRIORYTET | 
|---|-------|------|-----------|
|F-01|Definicja śledzonego produktu| Użytkownik musi mieć możliwość zdefiniowania nowego produktu/nawyku poprzez podanie: nazwy (np. "Papierosy"), jednostki miary (np. "paczka") oraz ceny jednostkowej.|1|
|F-02|Edycja ceny produktu| Użytkownik musi mieć możliwość aktualizacji ceny produktu. System musi zachować historię cen, aby stare wpisy były przeliczane po starej cenie, a nowe po nowej.|1|
|F-03|Zarządzanie listą produktów| Użytkownik może dodawać wiele niezależnych produktów (np. "Kawa", "Papierosy") i śledzić je równolegle.|2|
|F-04|Edycja parametrów historycznych| Możliwość wpisania, jak długo użytkownik już posiada dany nawyk, aby obliczyć stratę "wsteczną".|3|

(Priorytet: 1 - wymagane, 2 - przydatne, 3 - opcjonalne)

---

## Architektura systemu/oprogramowania

    
---

## Instalacja

### Wymagania wstępne

### Procedura instalacji

---

## Testy

---
