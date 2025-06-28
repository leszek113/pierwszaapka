#!/usr/bin/env python3
"""
Pierwszy skrypt Python w projekcie pierwszaapka
"""

import sys
import datetime

def main():
    """Główna funkcja programu"""
    print("=" * 50)
    print("Witaj w aplikacji pierwszaapka!")
    print("=" * 50)
    
    # Informacje o systemie
    print(f"Python version: {sys.version}")
    print(f"Data i czas: {datetime.datetime.now()}")
    print(f"Katalog roboczy: {sys.path[0]}")
    
    print("\nAplikacja działa poprawnie! 🎉")
    print("=" * 50)

if __name__ == "__main__":
    main() 