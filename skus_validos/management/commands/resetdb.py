import os
import subprocess
import psycopg2
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Reseta o banco de dados: limpa todas as tabelas e reinicia os IDs."

    def handle(self, *args, **kwargs):
        load_dotenv()
        db_engine = os.getenv("DB_ENGINE")
        database_url = os.getenv("DATABASE_URL")

        # Detectar tipo de banco pelo DATABASE_URL caso DB_ENGINE não esteja no .env
        if not db_engine and database_url:
            if database_url.startswith("sqlite"):
                db_engine = "django.db.backends.sqlite3"
            elif database_url.startswith("postgres"):
                db_engine = "django.db.backends.postgresql"

        if not db_engine:
            self.stdout.write(self.style.ERROR("❌ Não foi possível detectar o tipo de banco de dados. Verifique seu .env"))
            return

        if "sqlite3" in db_engine:
            self.reset_sqlite()
        elif "postgresql" in db_engine:
            self.reset_postgres()
        else:
            self.stdout.write(self.style.ERROR("❌ Banco de dados não suportado ou mal configurado."))

    def reset_sqlite(self):
        db_path = os.getenv("DB_NAME", "db.sqlite3")
        if os.path.exists(db_path):
            self.stdout.write(f"🗑️ Deletando {db_path}...")
            os.remove(db_path)

        self.stdout.write("⚙️ Rodando migrations...")
        subprocess.run(["python", "manage.py", "migrate"])
        self.stdout.write(self.style.SUCCESS("✅ SQLite resetado com sucesso."))

    def reset_postgres(self):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432"),
            )
            conn.autocommit = True
            cur = conn.cursor()

            self.stdout.write("🧹 Limpando tabelas do PostgreSQL...")

            cur.execute("""
            DO $$
            DECLARE
                r RECORD;
            BEGIN
                EXECUTE 'SET session_replication_role = replica';
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                    EXECUTE 'TRUNCATE TABLE ' || quote_ident(r.tablename) || ' RESTART IDENTITY CASCADE';
                END LOOP;
                EXECUTE 'SET session_replication_role = DEFAULT';
            END
            $$;
            """)

            cur.close()
            conn.close()
            self.stdout.write(self.style.SUCCESS("✅ PostgreSQL resetado com sucesso."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Erro ao conectar ou limpar o banco: {e}"))
