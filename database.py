
import sqlite3
from sqlite3 import Error
import os

# Define o caminho absoluto para o arquivo do banco de dados
DB_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "doc_agent.db"))

def create_connection():
    """Cria e retorna uma conexão com o banco de dados SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    return conn

def initialize_database():
    """
    Cria o banco de dados e as tabelas necessárias se elas ainda não existirem.
    """
    # SQL para criar a tabela de memória persistente
    sql_create_memory_table = """
    CREATE TABLE IF NOT EXISTS memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_name TEXT NOT NULL,
        key TEXT NOT NULL,
        value TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(agent_name, key)
    );
    """

    # SQL para criar a tabela de histórico de execuções
    sql_create_run_history_table = """
    CREATE TABLE IF NOT EXISTS run_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id TEXT NOT NULL,
        agent_name TEXT NOT NULL,
        input_data TEXT,
        output_data TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """

    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            print(f"Inicializando banco de dados em: {DB_FILE}")
            c.execute(sql_create_memory_table)
            c.execute(sql_create_run_history_table)
            conn.commit()
            print("Tabelas 'memory' e 'run_history' verificadas/criadas com sucesso.")
        except Error as e:
            print(f"Erro ao criar tabelas: {e}")
        finally:
            conn.close()
    else:
        print("Erro! Não foi possível criar a conexão com o banco de dados.")

if __name__ == '__main__':
    # Permite inicializar o banco de dados diretamente via linha de comando
    initialize_database()
