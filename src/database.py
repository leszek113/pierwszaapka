#!/usr/bin/env python3
"""
Skrypt do obslugi bazy danych SQLite
"""

import sqlite3
import os
from datetime import datetime

# Nazwa pliku bazy danych
DATABASE_FILE = 'pierwszaapka.db'

def create_database():
    """Tworzy baze danych i tabele jesli nie istnieja"""
    try:
        # Polacz z baza danych (utworzy plik jesli nie istnieje)
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        # Utworz tabele akcje
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS akcje (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT NOT NULL,
                cena REAL,
                yield TEXT,
                ocena TEXT,
                data_dodania TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Zatwierdz zmiany
        conn.commit()
        print(f"✅ Baza danych '{DATABASE_FILE}' utworzona/otwarta pomyslnie")
        print(f"✅ Tabela 'akcje' utworzona/istnieje")
        
        return conn
        
    except Exception as e:
        print(f"❌ Blad podczas tworzenia bazy danych: {e}")
        return None

def insert_akcje(conn, data):
    """Wstawia dane akcji do bazy danych"""
    try:
        cursor = conn.cursor()
        
        # Przygotuj dane do wstawienia (pomin naglowki)
        rows_to_insert = []
        for row in data[1:]:  # Pomijamy pierwszy wiersz (naglowki)
            if len(row) >= 4:  # Sprawdz czy wiersz ma wystarczajaca liczbe kolumn
                ticker = row[0]
                cena = float(row[1]) if row[1].replace('.', '').replace(',', '').isdigit() else None
                yield_val = row[2]
                ocena = row[3]
                
                rows_to_insert.append((ticker, cena, yield_val, ocena))
        
        # Wstaw dane
        cursor.executemany('''
            INSERT INTO akcje (ticker, cena, yield, ocena)
            VALUES (?, ?, ?, ?)
        ''', rows_to_insert)
        
        # Zatwierdz zmiany
        conn.commit()
        
        print(f"✅ Wstawiono {len(rows_to_insert)} rekordow do bazy danych")
        return True
        
    except Exception as e:
        print(f"❌ Blad podczas wstawiania danych: {e}")
        return False

def get_all_akcje(conn):
    """Pobiera wszystkie akcje z bazy danych"""
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM akcje ORDER BY data_dodania DESC')
        rows = cursor.fetchall()
        
        print(f"✅ Pobrano {len(rows)} rekordow z bazy danych")
        return rows
        
    except Exception as e:
        print(f"❌ Blad podczas pobierania danych: {e}")
        return []

def get_buy_recommendations(conn):
    """Pobiera tylko akcje z ocena 'kupuj'"""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM akcje 
            WHERE LOWER(ocena) = 'kupuj' 
            ORDER BY data_dodania DESC
        ''')
        rows = cursor.fetchall()
        
        print(f"✅ Pobrano {len(rows)} rekomendacji 'kupuj' z bazy danych")
        return rows
        
    except Exception as e:
        print(f"❌ Blad podczas pobierania rekomendacji: {e}")
        return []

def display_akcje(rows):
    """Wyswietla akcje w czytelny sposob"""
    if not rows:
        print("Brak danych do wyswietlenia")
        return
    
    print("\n" + "="*80)
    print("DANE Z BAZY SQLITE:")
    print("="*80)
    print(f"{'ID':<3} {'Ticker':<10} {'Cena':<8} {'Yield':<8} {'Ocena':<10} {'Data dodania':<20}")
    print("-" * 80)
    
    for row in rows:
        id_val, ticker, cena, yield_val, ocena, data_dodania = row
        cena_str = f"{cena:.2f}" if cena else "N/A"
        print(f"{id_val:<3} {ticker:<10} {cena_str:<8} {yield_val:<8} {ocena:<10} {data_dodania:<20}")

def clear_table(conn):
    """Czyści tabele akcje (usuwa wszystkie rekordy)"""
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM akcje')
        conn.commit()
        print("✅ Tabela 'akcje' zostala wyczyszczona")
        return True
        
    except Exception as e:
        print(f"❌ Blad podczas czyszczenia tabeli: {e}")
        return False

def main():
    """Glowna funkcja programu"""
    print("🚀 Uruchamianie skryptu bazy danych SQLite...")
    print("="*50)
    
    # Utworz/otworz baze danych
    conn = create_database()
    if not conn:
        return
    
    try:
        # Przyklad uzycia - mozesz to zmodyfikowac
        print("\n📊 Przyklad operacji na bazie danych:")
        print("1. Pobierz wszystkie akcje")
        print("2. Pobierz tylko rekomendacje 'kupuj'")
        print("3. Wyczysc tabele")
        
        # Pobierz wszystkie akcje
        all_akcje = get_all_akcje(conn)
        display_akcje(all_akcje)
        
        # Pobierz rekomendacje 'kupuj'
        buy_akcje = get_buy_recommendations(conn)
        if buy_akcje:
            print("\n" + "="*50)
            print("REKOMENDACJE 'KUPUJ' Z BAZY DANYCH:")
            print("="*50)
            display_akcje(buy_akcje)
        
    finally:
        # Zamknij polaczenie
        conn.close()
        print("\n🔒 Polaczenie z baza danych zamkniete")
    
    print("\n" + "="*50)
    print("✅ Skrypt bazy danych zakonczony pomyslnie!")

if __name__ == "__main__":
    main() 