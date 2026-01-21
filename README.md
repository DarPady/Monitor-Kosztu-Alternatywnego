# Monitor Kosztu Alternatywnego - MKA

 ## Table of Contents
- [Charakterystyka oprogramowania](#charakterystyk-oprogramowania)
- [Specyfikacja wymagań](#specyfikacja-wymagań)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)
- [Authorzy](#authorzy)

---

## Charakterystyka oprogramowania
Projekt bada koszt alternatywny w kontekście osobistych finansów i ekonomii behawioralnej, ilościowo przedstawiając realne skutki utrwalonych, drobnych nawyków konsumpcyjnych, takich jak codzienne wydatki na używki czy drobne zakupy. Aplikacja pozwala użytkownikowi zobaczyć, jak mikro-decyzje finansowe wpływają na długoterminowy, skumulowany potencjał inwestycyjny, ułatwiając świadome podejmowanie decyzji i lepsze zarządzanie własnym budżetem.

Produktem końcowym jest interaktywna aplikacja webowa w formie pulpitu (dashboard), wyróżniająca się pełną personalizacją śledzonych nawyków oraz przeliczaniem codziennych wydatków na aktualną wartość potencjalnych inwestycji. Celem projektu jest nie tylko edukacja użytkowników w zakresie finansów osobistych, ale także pokazanie realnego wpływu codziennych wydatków na długoterminowy potencjał inwestycyjny.


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

## Technologies Used

    
---

## Installation

### Prerequisites

### Steps

---

## Usage

---

## Folder Structure

---

## Contributing

---

## Prawa  autorskie
**Monitor Kosztu Alternatywnego (MKA)** to projekt edukacyjny opracowany w ramach kursu inżynierii oprogramowania na Uniwersytecie Gdańskim.

Oprogramowanie jest dostępne bezpłatnie i może być pobierane, używane i modyfikowane wyłącznie **w celach edukacyjnych i osobistych.** Wszelkie wykorzystanie komercyjne jest surowo zabronione, w tym sprzedaż oprogramowania, czerpanie zysków z jego dystrybucji lub włączanie go do płatnych pakietów oprogramowania. Aplikacja może być dystrybuowana wyłącznie w bezpłatnej, niekomercyjnej formie.

Aplikacja pobiera dane rynkowe z serwisu **Bankier.pl** w celach analitycznych. Wszelkie prawa do danych rynkowych należą do ich odpowiednich dostawców. Autor nie rości sobie prawa własności do pobranych danych i udostępnia jedynie narzędzie do ich automatycznego agregowania w celu analizy osobistej. Wszelkie komercyjne wykorzystanie pobranych danych może wymagać oddzielnego zezwolenia od dostawcy danych.

Autor nie gwarantuje, że oprogramowanie jest wolne od błędów i nie ponosi odpowiedzialności za jakiekolwiek szkody lub decyzje inwestycyjne podjęte na podstawie wyników lub symulacji wygenerowanych przez aplikację.


---

## Authorzy
Jeśli masz jakieś pytania lub sugestie, skontaktuj się z nami:
- **Profil  GitHub**: Daria Padytel - [DarPady](https://github.com/DarPady)
                      Julia Rutkowska - [rutkowskaj](https://github.com/rutkowskaj)
                      Katarzyna Zaniewska - [KatarzynaZaniewska](https://github.com/KatarzynaZaniewska)
