#!/usr/bin/env python3
"""
Aplikacja webowa Flask do wyświetlania danych z bazy SQLite
"""

from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Nazwa pliku bazy danych
DATABASE_FILE = 'pierwszaapka.db'

def get_db_connection():
    """Tworzy polaczenie z baza danych"""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # Pozwala na dostep do kolumn przez nazwy
    return conn

def get_all_akcje():
    """Pobiera wszystkie akcje z bazy danych"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM akcje ORDER BY data_dodania DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_akcje_by_filter(filter_type):
    """Pobiera akcje wedlug filtru"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if filter_type == 'kupuj':
        cursor.execute('''
            SELECT * FROM akcje 
            WHERE LOWER(ocena) = 'kupuj' 
            ORDER BY data_dodania DESC
        ''')
    elif filter_type == 'sprzedaj':
        cursor.execute('''
            SELECT * FROM akcje 
            WHERE LOWER(ocena) = 'sprzedaj' 
            ORDER BY data_dodania DESC
        ''')
    elif filter_type == 'trzymaj':
        cursor.execute('''
            SELECT * FROM akcje 
            WHERE LOWER(ocena) = 'trzymaj' 
            ORDER BY data_dodania DESC
        ''')
    else:
        cursor.execute('SELECT * FROM akcje ORDER BY data_dodania DESC')
    
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route('/')
def index():
    """Strona glowna"""
    filter_type = request.args.get('filter', 'all')
    akcje = get_akcje_by_filter(filter_type)
    return render_template('index.html', akcje=akcje, current_filter=filter_type)

@app.route('/api/akcje')
def api_akcje():
    """API endpoint do pobierania danych w formacie JSON"""
    filter_type = request.args.get('filter', 'all')
    akcje = get_akcje_by_filter(filter_type)
    
    # Konwertuj na liste slownikow
    akcje_list = []
    for akcja in akcje:
        akcje_list.append({
            'id': akcja['id'],
            'ticker': akcja['ticker'],
            'cena': akcja['cena'],
            'yield': akcja['yield'],
            'ocena': akcja['ocena'],
            'data_dodania': akcja['data_dodania']
        })
    
    return jsonify(akcje_list)

@app.route('/stats')
def stats():
    """Strona ze statystykami"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Liczba wszystkich akcji
    cursor.execute('SELECT COUNT(*) FROM akcje')
    total_count = cursor.fetchone()[0]
    
    # Liczba akcji wedlug oceny
    cursor.execute('''
        SELECT ocena, COUNT(*) as count 
        FROM akcje 
        GROUP BY ocena
    ''')
    oceny_stats = cursor.fetchall()
    
    # Srednia cena
    cursor.execute('SELECT AVG(cena) FROM akcje WHERE cena IS NOT NULL')
    avg_price = cursor.fetchone()[0]
    
    conn.close()
    
    return render_template('stats.html', 
                         total_count=total_count,
                         oceny_stats=oceny_stats,
                         avg_price=avg_price)

if __name__ == '__main__':
    print("🚀 Uruchamianie aplikacji webowej Flask...")
    print("🌐 Aplikacja bedzie dostepna pod adresem: http://localhost:8080")
    print("="*50)
    
    # Sprawdz czy baza danych istnieje
    if not os.path.exists(DATABASE_FILE):
        print(f"❌ Baza danych '{DATABASE_FILE}' nie istnieje!")
        print("Uruchom najpierw: python src/sync_data.py")
    else:
        print(f"✅ Znaleziono baze danych: {DATABASE_FILE}")
        app.run(debug=True, host='0.0.0.0', port=8080) 