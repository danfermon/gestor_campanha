import os
import subprocess
import psycopg2
import sqlite3
from dotenv import load_dotenv

#python reset_database.py

# Carrega as variáveis do .env
load_dotenv()

DB_ENGINE = os.getenv("DB_ENGINE")

def reset_sqlite():
    db_path = os.getenv("DB_NAME", "db.sqlite3")
    if os.path.exists(db_path):
        print(f"Deletando {db_path}...")
        os.remove(db_path)
    print("Rodando migrations...")
    subprocess.run(["python", "manage.py", "migrate"])
    print("SQLite resetado com sucesso.")

def reset_postgres():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
    )
    conn.autocommit = True
    cur = conn.cursor()
    print("Limpando tabelas do PostgreSQL...")

    cur.execute("""
    DO $$
    DECLARE
        r RECORD;
    BEGIN
        -- Desativa constraints
        EXECUTE 'SET session_replication_role = replica';

        -- Trunca todas as tabelas com reset de IDs
        FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
            EXECUTE 'TRUNCATE TABLE ' || quote_ident(r.tablename) || ' RESTART IDENTITY CASCADE';
        END LOOP;

        -- Ativa constraints novamente
        EXECUTE 'SET session_replication_role = DEFAULT';
    END
    $$;
    """)
    cur.close()
    conn.close()
    print("PostgreSQL resetado com sucesso.")

if __name__ == "__main__":
    if "sqlite3" in DB_ENGINE:
        reset_sqlite()
    elif "postgresql" in DB_ENGINE:
        reset_postgres()
    else:
        print("Banco de dados não suportado ou mal configurado.")
