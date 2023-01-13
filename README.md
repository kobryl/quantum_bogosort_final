# quantum_bogosort_final (Znajdź drogę do celu)

Zadanie finałowe na BEST Coding Marathon 2023. Aplikacja służy do wyszukiwania najszybszej trasy komunikacją miejską w Gdańsku (lub pieszo) z jednego przystannku na drugi.

## :writing_hand: Autorzy

Drużyna Quantum Bogosort:
- Konrad Bryłowski
- Aleksander Czerwionka
- Michał Krause
- Łukasz Nowakowski

## Działanie programu

Interfejs graficzny został zrealizowany jako aplikacja webowa - użytkownik wprowadza przystanek startowy i końcowy oraz dodatkowe parametry - maksymalna liczba przesiadek, maksymalny czas oczekiwania na przesiadkę oraz maksymalny dystans do pokonania pieszo przy przechodzeniu między przystankami.

## Uruchomienie aplikacji

Należy uruchomić serwer Django w pythonie:

    py manage.py runserver

Aplikacja wykorzystuje dane zawarte w repozytorium otwartych danych ZTM w Gdańsku. 

Dane wykorzystywane przez część napisaną w pythonie są dynamicznie pobierane z repozytorium. Część napisana w C++ korzysta z plików txt w katalogu `gtfsgoogle`. Do ich aktualizacji służy skrypt `update_files.py`, który należy umieścić w Harmonogramie zadań (Windows) lub crontabie (Linux) w celu jego uruchamiania raz na dobę - dane w tych plikach nie wymagają tak częstej aktualizacji jak pliki JSON.

## Użyte technologie

- python
- Django
- C++
- HTML, JS i CSS