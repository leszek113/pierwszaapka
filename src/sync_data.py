#!/usr/bin/env python3
"""
Skrypt do synchronizacji danych z Google Sheets do SQLite
"""

import os
import sys

# Dodaj katalog src do sciezki Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from google_sheets import load_credentials, get_sheets_data
from database import create_database, insert_akcje, get_all_akcje, display_akcje, clear_table

def sync_google_sheets_to_sqlite():
    """Synchronizuje dane z Google Sheets do bazy SQLite"""
    print("🔄 Rozpoczynam synchronizacje danych...")
    print("="*50)
    
    # Krok 1: Pobierz dane z Google Sheets
    print("📊 Krok 1: Pobieranie danych z Google Sheets...")
    credentials = load_credentials()
    if not credentials:
        print("❌ Nie udalo sie zaladowac danych uwierzytelniajacych")
        return False
    
    sheets_data = get_sheets_data(credentials)
    if not sheets_data:
        print("❌ Nie udalo sie pobrac danych z Google Sheets")
        return False
    
    print(f"✅ Pobrano {len(sheets_data)} wierszy z Google Sheets")
    
    # Krok 2: Polacz z baza danych
    print("\n💾 Krok 2: Laczenie z baza danych SQLite...")
    conn = create_database()
    if not conn:
        print("❌ Nie udalo sie polaczyc z baza danych")
        return False
    
    try:
        # Krok 3: Wyczysc stara tabele (opcjonalnie)
        print("\n🧹 Krok 3: Czyszczenie starej tabeli...")
        clear_table(conn)
        
        # Krok 4: Wstaw nowe dane
        print("\n📝 Krok 4: Wstawianie danych do bazy...")
        if insert_akcje(conn, sheets_data):
            print("✅ Dane zostaly pomyslnie wstawione do bazy")
        else:
            print("❌ Blad podczas wstawiania danych")
            return False
        
        # Krok 5: Sprawdz wyniki
        print("\n🔍 Krok 5: Sprawdzanie wynikow...")
        all_akcje = get_all_akcje(conn)
        display_akcje(all_akcje)
        
        print("\n" + "="*50)
        print("✅ Synchronizacja zakonczona pomyslnie!")
        return True
        
    finally:
        conn.close()
        print("🔒 Polaczenie z baza danych zamkniete")

def main():
    """Glowna funkcja programu"""
    print("🚀 Uruchamianie synchronizacji Google Sheets -> SQLite...")
    print("="*60)
    
    success = sync_google_sheets_to_sqlite()
    
    if success:
        print("\n🎉 Wszystko dziala poprawnie!")
        print("📊 Dane z Google Sheets zostaly zapisane w bazie SQLite")
    else:
        print("\n❌ Wystapil blad podczas synchronizacji")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main() 