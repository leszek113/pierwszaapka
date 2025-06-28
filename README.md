# Aplikacja Google Sheets → SQLite → Web

## Opis projektu
Aplikacja Python, która:
- Pobiera dane z Google Sheets
- Zapisuje je w bazie SQLite
- Wyświetla dane przez interfejs webowy

## Struktura projektu
```
pierwszaapka/
├── src/          # Główny kod aplikacji
├── tests/        # Testy
├── config/       # Konfiguracja
└── docs/         # Dokumentacja
```

## Status
Projekt w trakcie rozwoju...

---

## Jak uruchomić projekt po restarcie komputera

1. **Otwórz terminal i przejdź do katalogu projektu:**
   ```bash
   cd /Users/leszek/Coursor/pierwszaapka
   ```

2. **Aktywuj środowisko wirtualne:**
   ```bash
   source venv/bin/activate
   ```
   (Po tej komendzie powinno pojawić się `(venv)` na początku linii terminala)

3. **(Opcjonalnie) Zaktualizuj dane z Google Sheets:**
   ```bash
   python3 src/sync_data.py
   ```

4. **Uruchom aplikację webową:**
   ```bash
   python3 src/app.py
   ```
   Aplikacja będzie dostępna pod adresem:  
   [http://localhost:8080](http://localhost:8080)

5. **Aby zatrzymać aplikację:**  
   Wciśnij `Ctrl+C` w terminalu.

---

**Wskazówki:**
- Jeśli pojawi się błąd o braku bibliotek, upewnij się, że aktywowałeś środowisko wirtualne (`source venv/bin/activate`).
- Jeśli chcesz zaktualizować dane z Google Sheets, uruchom najpierw `python3 src/sync_data.py`, a potem `python3 src/app.py`. 