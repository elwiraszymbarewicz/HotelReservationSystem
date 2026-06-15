# 🛏️ System Zarządzania Hotelem v1.2 Premium

Nowoczesna aplikacja okienkowa służąca do kompleksowej i zautomatyzowanej obsługi procesów hotelowych. System pozwala na sprawną rejestrację gości, zarządzanie strukturą pokoi, dynamiczne rezerwowanie terminów oraz natychmiastowe wystawianie dokumentów księgowych.

---

## 🛠️ Wymagania projektu

Zgodnie z wytycznymi technicznymi, aplikacja została zaprojektowana w oparciu o architekturę wieloplikową z zachowaniem jawnego podziału na logikę biznesową (Model Dziedzinowy) oraz warstwę prezentacji (GUI):

* **Język programowania:** Python 3.10+
* **Framework GUI:** Tkinter & TTK Themes (wbudowany pakiet standardowy)
* **Środowisko testowe:** Pytest 9.1+ (automatyczne testy regresyjne)
* **Zależności systemowe:** Zgodne z plikiem `requirements.txt` (środowisko `pytest` oraz wtyczki)

---

## 🚀 Opis funkcjonalności

System realizuje pełen cykl obsługi klienta hotelowego za pomocą czterech zintegrowanych modułów:

1. **Panel Gości:** Umożliwia rejestrację danych osobowych (imię, e-mail, telefon, dokument) przy użyciu metod walidacji formatu adresu e-mail oraz kompletności wprowadzonych pól.
2. **Wykaz Pokoi:** Zarządzanie strukturą i standardem pokoi (Standard, Deluxe, Suite). Tabela posiada interaktywną funkcję zmiany stanu czystości (Double-Click przełącza status pokoju pomiędzy czystym a wymagającym sprzątania).
3. **Grafik Rezerwacji:** Zaawansowany algorytm weryfikujący dostępność zasobów w czasie. System automatycznie blokuje i odrzuca próby rezerwacji, które generują konflikty terminów lub nakładanie się dat dla tego samego pokoju.
4. **Księgowość i Finanse:** Automatyczne generowanie faktur powiązanych bezpośrednio z kartą rezerwacji. Należność finansowa jest kalkulowana dynamicznie na podstawie stawki za noc oraz długości pobytu.

---

## 👥 Opis zespołu i obowiązków

Praca nad projektem została zrealizowana w strukturze rozproszonej przy użyciu gałęzi funkcjonalnych (Feature Branches) oraz procedury Code Review w repozytorium GitHub:

* **Elwira:** Projekt i implementacja fundamentów modelu dziedzinowego (klasy `Guest` i `Room`), stworzenie metod walidacji danych wejściowych oraz przygotowanie całościowej architektury nowoczesnego interfejsu graficznego (GUI).
* **Karolina:** Implementacja modułu rezerwacji (klasa `Reservation`), oprogramowanie logiki kalkulacji kosztów pobytu oraz mechanizmu bezpiecznego anulowania rezerwacji.
* **Natalia:** Zaprojektowanie i wdrożenie podsystemu finansowego (klasa `Invoice`), logiki generowania tekstowych podsumowań rachunków oraz zarządzania statusami płatności.
* **Wiktoria:** Stworzenie głównego kontrolera zarządzającego (`HotelManager`), implementacja algorytmu bezkonfliktowego badania zajętości terminów oraz przygotowanie zestawu automatycznych testów integracyjnych.

---

## 📦 Instalacja (wymagane biblioteki, itp.)

### 1. Pobranie projektu z repozytorium
Otwórz terminal w wybranym folderze i sklonuj projekt komendą:
`git clone https://github.com/elwiraszymbarewicz/HotelReservationSystem.git`
`cd HotelReservationSystem`

### 2. Tworzenie i aktywacja środowiska wirtualnego (Zalecane)
Aby uniknąć konfliktów z globalnymi pakietami w systemie, utwórz i aktywuj odizolowane środowisko wirtualne `venv`:

**System Windows:**
`python -m venv venv`
`.\venv\Scripts\activate`

**System macOS / Linux:**
`python3 -m venv venv`
`source venv/bin/activate`

### 3. Instalacja zależności i środowiska testowego
Gdy środowisko wirtualne jest aktywne (w terminalu pojawi się znacznik `(venv)`), zainstaluj wszystkie wymagane pakiety i narzędzia testowe z pliku konfiguracyjnego za pomocą menedżera pakietów pip:
`pip install --upgrade pip`
`pip install -r requirements.txt`

---

## 💻 Przykłady wykorzystania

### 1. Uruchomienie aplikacji okienkowej GUI
Główny interfejs systemu zarządzania hotelem uruchamiamy jako moduł Pythona wpisując w terminalu:
`python -m src.gui_app`

### 2. Wywołanie automatycznej weryfikacji (Testy)
Aby uruchomić testy jednostkowe i integracyjne sprawdzające poprawność działania wszystkich funkcji, użyj komendy:
`pytest`

### 3. Scenariusz biznesowy (Jak działa system w praktyce)
System służy do prowadzenia recepcji hotelowej. Poniżej opisano kompletny, zaimplementowany proces obsługi:

* **Krok 1: Przyjęcie nowego gościa (Check-in)**
  W zakładce "Goście" recepcjonista wprowadza dane klienta (np. Jan Kowalski, jan@wp.pl). System sprawdza poprawność adresu e-mail. Po zatwierdzeniu, gość otrzymuje w bazie unikalny identyfikator (np. `ID: 1`).
  
* **Krok 2: Konfiguracja oferty pokojowej**
  W zakładce "Pokoje" definiujemy dostępne pokoje (np. Pokój numer `101`, klasa `Deluxe`, cena `300.00 PLN`). Nowo dodany pokój automatycznie pojawia się na liście jako "Czysty".
  
* **Krok 3: Rezerwacja bezkonfliktowa**
  W zakładce "Rezerwacje" łączymy zasoby wpisując ID Gościa (`1`) oraz Numer Pokoju (`101`) i wybieramy termin. System kalkuluje koszt. Jeśli spróbujemy dodać innego gościa do pokoju `101` w tym samym terminie, wbudowany algorytm menedżera zablokuje operację i wyświetli komunikat o kolizji dat.
  
* **Krok 4: Cykl życia pokoju**
  Po opuszczeniu pokoju przez gościa, recepcjonista klika dwukrotnie w wiersz pokoju na liście, zmieniając jego status na "Wymaga sprzątania" (wiersz podświetla się na czerwono). Po posprzątaniu, kolejne dwukrotne kliknięcie przywraca status "Czysty" (zielony akcent).
  
* **Krok 5: Rozliczenie (Wystawienie faktury)**
  W zakładce "Finanse i Faktury" wprowadzamy ID zakończonej rezerwacji. System automatycznie pobiera dane gościa, wylicza finalną kwotę na podstawie liczby spędzonych nocy i generuje oficjalny dokument z unikalnym numerem (np. `FV/500`) ze statusem "Nieopłacona". Po uregulowaniu należności, dwukrotne kliknięcie oznacza fakturę jako "OPŁACONA".

  ---
  ## 📷 Wizualna dokumentacja systemu (Zrzuty ekranu)
Poniżej znajdują się zrzuty ekranu prezentujące działanie gotowanego programu z nowoczesnym, ciemnym motywem graficznym:
<img width="1896" height="1294" alt="image" src="https://github.com/user-attachments/assets/b69a7009-a52b-49b1-9fed-f556e3796f45" />
<img width="1882" height="1302" alt="image" src="https://github.com/user-attachments/assets/cae9e062-e6e0-49f9-8f2c-4f47544acce9" />
<img width="1896" height="1300" alt="image" src="https://github.com/user-attachments/assets/1d3356e6-15e8-48aa-a81d-cc79601479ea" />
<img width="1896" height="1310" alt="image" src="https://github.com/user-attachments/assets/0c276024-957b-4069-8e36-34242d54553a" />



