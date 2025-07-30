from django.core.management.base import BaseCommand
from skus_validos.models import Skus_validos
from django.db import connection
from django.conf import settings

class Command(BaseCommand):
    help = 'Deleta todos os SKUs válidos e reseta o ID'

    def handle(self, *args, **options):
        # Proteção para só rodar em ambiente de desenvolvimento
        if not settings.DEBUG:
            self.stdout.write(self.style.ERROR("Esse comando só pode ser executado em ambiente de desenvolvimento."))
            return

        self.stdout.write("Deletando todos os SKUs...")
        Skus_validos.objects.all().delete()

        table_name = Skus_validos._meta.db_table

        with connection.cursor() as cursor:
            if 'sqlite' in connection.settings_dict['ENGINE']:
                cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")
                self.stdout.write("Autoincremento resetado (SQLite).")
            elif 'postgresql' in connection.settings_dict['ENGINE']:
                cursor.execute(f"ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1;")
                self.stdout.write("Autoincremento resetado (PostgreSQL).")
            elif 'mysql' in connection.settings_dict['ENGINE']:
                cursor.execute(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1;")
                self.stdout.write("Autoincremento resetado (MySQL).")
            else:
                self.stdout.write("Banco não suportado para resetar autoincremento.")

        self.stdout.write(self.style.SUCCESS("SKUs deletados e IDs resetados com sucesso."))
