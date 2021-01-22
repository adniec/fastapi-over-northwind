### Mikroserwisowa aplikacja do łączenia się z bazą "Northwind" w oparciu o PostgreSQL oraz FastApi

![Diagram](docs/img/ER.png)

### Dokumentacja

- [Instrukcja](docs/Instrukcja.md) użytkownika
- [Prezentacja](docs/Wprowadzenie.pdf) projektu i technologii
- [Przewodnik](docs/Przewodnik.md) po wykorzystywanej technologii
- [Realizacja](docs/Zamawianie.md) zamawiania produktów
- Pomiary:
    - [Opis](docs/Pomiary-opis.md) wykonywania pomiarów
    - [Pomiary](docs/Pomiary-crud.md) CRUD'u na tabeli products
    - [Pomiary](docs/Pomiary-crud.md) z wykonania raportów
    - [Wnioski](docs/Pomiary-wnioski.md) z pomiarów

### Struktura projektu

Główny folder zawiera pliki niezbędne do stworzenia bazy, na której będziemy operować oraz przygotowania środowiska 
pracy. Znajdziemy w nim pliki konfiguracyjne takie jak: [docker-compose.yml](docker-compose.yml) umożliwiający 
dostosowanie kontenerów czy [nginx_config.conf](nginx_config.conf) odpowiedzialny za ustawienia serwera. Znajduje się 
tu również plik [northwind.sql](northwind.sql), dzięki któremu tworzona jest nasza baza.

Folder `docs` zawiera dokumentację uzyskaną podczas rozwijania projektu.

Serwisy komunikujące się z bazą danych są dodane w odpowiednich folderach, przykładowo `auth-service`.

### Realizacja

- Adrian Nieć
