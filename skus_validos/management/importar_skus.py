import json
import os
from django.core.management.base import BaseCommand
from skus_validos.models import Skus_validos

class Command(BaseCommand):
    help = 'Importa dados do JSON para a tabela Skus_validos'

    def add_arguments(self, parser):
        parser.add_argument('--arquivo', type=str, help='Caminho para o arquivo JSON', required=True)

    def handle(self, *args, **kwargs):
        caminho_arquivo = kwargs['arquivo']

        if not os.path.exists(caminho_arquivo):
            self.stdout.write(self.style.ERROR(f'Arquivo {caminho_arquivo} não encontrado.'))
            return

        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            dados_json = json.load(f)

        registros = []

        def parse_linha(linha):
            partes = linha.split(';')
            if len(partes) == 4:
                return {
                    'nome': partes[0].strip(),
                    'ean': partes[1].strip(),
                    'dun': partes[2].strip(),
                    'categoria': partes[3].strip()
                }
            return None

        for item in dados_json:
            if "Nome;Ean;Dun;Categoria" in item:
                principal = parse_linha(item["Nome;Ean;Dun;Categoria"])
                if principal:
                    registros.append(principal)

            if "null" in item:
                for sub in item["null"]:
                    sub_item = parse_linha(sub)
                    if sub_item:
                        registros.append(sub_item)

        inseridos = 0
        for registro in registros:
            Skus_validos.objects.create(
                nome=registro['nome'],
                ean=registro['ean'],
                dun=registro['dun'],
                categoria=registro['categoria']
            )
            inseridos += 1

        self.stdout.write(self.style.SUCCESS(f'{inseridos} registros inseridos com sucesso.'))
