"""
Setup de banco de dados simples para testes do frontend
Cria sessão mock para evitar dependências complexas
"""

import sqlite3
import os
from contextlib import contextmanager

class MockDB:
    """Classe mock para simular sessão de banco de dados nos testes"""
    
    def __init__(self):
        self.db_path = "/tmp/helio_test.db"
        self._init_db()
    
    def _init_db(self):
        """Inicializa banco SQLite simples para testes"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabelas básicas para testes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                email TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mpc_palavras_chave (
                id INTEGER PRIMARY KEY,
                usuario_id INTEGER,
                area_interesse TEXT,
                cargo_objetivo TEXT,
                status TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vagas_analisadas (
                id INTEGER PRIMARY KEY,
                mpc_id INTEGER,
                titulo TEXT,
                empresa TEXT,
                descricao TEXT,
                fonte TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    @contextmanager
    def get_session(self):
        """Retorna contexto de sessão mock"""
        yield MockSession()

class MockSession:
    """Sessão mock que simula operações de banco"""
    
    def query(self, model):
        return MockQuery()
    
    def add(self, obj):
        pass
    
    def commit(self):
        pass
    
    def close(self):
        pass

class MockQuery:
    """Query mock para simular consultas"""
    
    def filter(self, *args):
        return self
    
    def first(self):
        return None
    
    def all(self):
        return []
    
    def limit(self, n):
        return self
    
    def order_by(self, *args):
        return self

# Instância global para uso nos testes
mock_db = MockDB()

def get_test_session():
    """Retorna sessão de teste"""
    return mock_db.get_session()