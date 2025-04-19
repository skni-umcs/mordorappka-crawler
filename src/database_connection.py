import psycopg2
from psycopg2 import OperationalError
import threading
import os
from dotenv import load_dotenv
from typing import Optional, List, Tuple, Any, Union


class DatabaseConnection:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'connection'):
            try:
                # Ładowanie zmiennych środowiskowych
                load_dotenv()
                
                # Łączenie z bazą danych
                self.connection = psycopg2.connect(
                    host=os.getenv("DATABASE_HOST"),
                    port=os.getenv("DATABASE_PORT"),
                    dbname=os.getenv("DATABASE_NAME"),
                    user=os.getenv("DATABASE_USERNAME"),
                    password=os.getenv("DATABASE_PASSWORD")
                )
                self.cursor = self.connection.cursor()
                print("[+] Połączono z bazą danych.")
            except OperationalError as e:
                print(f"[!] Błąd połączenia z bazą danych: {e}")
                raise
    
    def execute(self, query: str, params: Optional[Union[tuple, dict]] = None) -> None:
        """
        Wykonuje zapytanie SQL.
        
        Args:
            query: Zapytanie SQL do wykonania
            params: Parametry zapytania (opcjonalne)
        """
        try:
            self.cursor.execute(query, params)
        except Exception as e:
            print(f"[!] Błąd wykonania zapytania: {e}")
            raise
    
    def execute_many(self, query: str, params_list: List[tuple]) -> None:
        """
        Wykonuje wiele zapytań SQL z listą parametrów.
        
        Args:
            query: Zapytanie SQL do wykonania
            params_list: Lista krotek z parametrami
        """
        try:
            self.cursor.executemany(query, params_list)
        except Exception as e:
            print(f"[!] Błąd wykonania masowego zapytania: {e}")
            raise
    
    def fetchone(self) -> Optional[Tuple]:
        """
        Pobiera jeden wiersz wyników zapytania.
        
        Returns:
            Pojedynczy wiersz wyników lub None
        """
        return self.cursor.fetchone()
    
    def fetchall(self) -> List[Tuple]:
        """
        Pobiera wszystkie wiersze wyników zapytania.
        
        Returns:
            Lista wierszy wyników
        """
        return self.cursor.fetchall()
    
    def commit(self) -> None:
        """
        Zatwierdza transakcję.
        """
        self.connection.commit()
    
    def rollback(self) -> None:
        """
        Wycofuje transakcję w przypadku błędu.
        """
        self.connection.rollback()
    
    def close(self) -> None:
        """
        Zamyka połączenie z bazą danych.
        """
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
        print("[x] Połączenie z bazą danych zamknięte.")
    
    def __del__(self) -> None:
        """
        Destruktor klasy, zapewnia zamknięcie połączenia.
        """
        self.close()