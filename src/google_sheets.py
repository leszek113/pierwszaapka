#!/usr/bin/env python3
"""
Skrypt do pobierania danych z Google Sheets
"""

import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ID arkusza Google Sheets
SPREADSHEET_ID = '1y4I-0Evf56NGaWGnkELVPm7p66hywzLA8LLeviqkvhw'

# Zakres danych do pobrania (wszystkie dane z arkusza)
RANGE_NAME = 'Sheet1!A:Z'

def load_credentials():
    """Laduje dane uwierzytelniajace z pliku JSON"""
    try:
        # Sciezka do pliku z kluczami
        credentials_path = os.path.join('config', 'pierwszaapka-464314-9c00bd4d0038.json')
        
        # Sprawdz czy plik istnieje
        if not os.path.exists(credentials_path):
            print(f"❌ Blad: Plik {credentials_path} nie istnieje!")
            return None
        
        # Zaladuj dane uwierzytelniajace
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        
        print("✅ Dane uwierzytelniajace zaladowane pomyslnie")
        return credentials
        
    except Exception as e:
        print(f"❌ Blad podczas ladowania danych uwierzytelniajacych: {e}")
        return None

def get_sheets_data(credentials):
    """Pobiera dane z Google Sheets"""
    try:
        # Utworz serwis Google Sheets
        service = build('sheets', 'v4', credentials=credentials)
        
        print(f"🔗 Laczenie z arkuszem: {SPREADSHEET_ID}")
        
        # Pobierz dane
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
        ).execute()
        
        values = result.get('values', [])
        
        if not values:
            print("⚠️  Arkusz jest pusty!")
            return []
        
        print(f"✅ Pobrano {len(values)} wierszy danych")
        return values
        
    except Exception as e:
        print(f"❌ Blad podczas pobierania danych: {e}")
        return []

def filter_buy_recommendations(data):
    """Filtruje wiersze z ocena 'kupuj'"""
    if not data:
        return []
    
    # Pierwszy wiersz to naglowki
    headers = data[0]
    
    # Znajdz indeks kolumny 'ocena'
    try:
        ocena_index = headers.index('ocena')
    except ValueError:
        print("❌ Nie znaleziono kolumny 'ocena' w naglowkach")
        return []
    
    # Filtruj wiersze z ocena 'kupuj'
    buy_recommendations = []
    for i, row in enumerate(data[1:], start=2):  # start=2 bo pomijamy naglowki
        if len(row) > ocena_index and row[ocena_index].lower() == 'kupuj':
            buy_recommendations.append(row)
    
    return buy_recommendations

def display_data(data):
    """Wyswietla pobrane dane"""
    if not data:
        print("Brak danych do wyswietlenia")
        return
    
    print("\n" + "="*50)
    print("WSZYSTKIE DANE Z GOOGLE SHEETS:")
    print("="*50)
    
    for i, row in enumerate(data):
        print(f"Wiersz {i+1}: {row}")
    
    # Filtruj i wyswietl tylko rekomendacje "kupuj"
    buy_recommendations = filter_buy_recommendations(data)
    
    print("\n" + "="*50)
    print("REKOMENDACJE 'KUPUJ':")
    print("="*50)
    
    if buy_recommendations:
        headers = data[0]  # Naglowki z pierwszego wiersza
        print(f"Naglowki: {headers}")
        print("-" * 50)
        
        for i, row in enumerate(buy_recommendations, start=1):
            print(f"Rekomendacja {i}: {row}")
        
        print(f"\n✅ Znaleziono {len(buy_recommendations)} rekomendacji 'kupuj'")
    else:
        print("❌ Nie znaleziono zadnych rekomendacji 'kupuj'")

def main():
    """Glowna funkcja programu"""
    print("🚀 Uruchamianie skryptu Google Sheets...")
    print("="*50)
    
    # Zaladuj dane uwierzytelniajace
    credentials = load_credentials()
    if not credentials:
        return
    
    # Pobierz dane z arkusza
    data = get_sheets_data(credentials)
    
    # Wyswietl dane
    display_data(data)
    
    print("\n" + "="*50)
    print("✅ Skrypt zakonczony pomyslnie!")

if __name__ == "__main__":
    main() 