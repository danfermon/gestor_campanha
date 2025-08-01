# funções gerais para uso em todo o projeto - Danny - 27-06-2025

import requests
import json
import os
import re

from django.core.management.base import BaseCommand
from skus_validos.models import Skus_validos
from django.db import connection
from django.conf import settings

from PIL import Image
import pytesseract

import re

def retorna_atividades(nivel):
    
    if nivel == "1":
        #admin
        atividades = ('Gerenciar o próprio perfil',
                      'Gerenciar Usuários', 
                      'Gerenciar Participantes', 
                      'Gerar Relatórios', 
                      'Gerar Sorteios', 
                      'Gerar Números da Sorte',
                      'Visualizar Dashboard')
    if nivel == "2" :
        # comum
        atividades = ('Gerenciar o próprio perfil',
                      'Gerar Relatórios'
                      'Visualizar Dashboard')
        
    if nivel == "3" :
        # visitante
        atividades = ('Gerenciar o próprio perfil',
                      'Visualizar Dashboard')
    
    return atividades

def ValidaSenha():
    ...


def retorna_participante():
    ...

def retorna_cep(cep):
    # chamar a api de cep para preencher os campos de endereco
    url = 'https://viacep.com.br/ws/'+cep+'/json'
    campos = requests.get(url)

    if campos.status_code == 200:
        print(campos.json())
        return campos.json()
    else:
        print(campos.status_code)
        return campos.status_code

def importar_csv(arq):
    # Define o caminho completo da pasta
    caminho_da_pasta = "static/csv"  
    nome_do_arquivo = arq
    caminho_completo = os.path.join(caminho_da_pasta, nome_do_arquivo)

    # Cria a pasta se ela não existir
    if not os.path.exists(caminho_da_pasta):
        os.makedirs(caminho_da_pasta)

    try:
        # Abre o arquivo para escrita (cria se não existir)
        with open(caminho_completo, "w") as arquivo:
            # Escreve no arquivo
            arquivo.write("Este é um exemplo de texto.")
        print(f"Arquivo '{nome_do_arquivo}' salvo em '{caminho_da_pasta}'")
        return caminho_da_pasta + '/' + nome_do_arquivo
    except Exception as e:
        print(f"Ocorreu um erro ao salvar o arquivo: {e}")


def limpar_lista_sku(table_name):
     with connection.cursor() as cursor:
            if 'sqlite' in connection.settings_dict['ENGINE']:
                cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")
                retorno = "Autoincremento resetado (SQLite)."
                msg = 'SKUs deletados e IDs resetados com sucesso.'

            elif 'postgresql' in connection.settings_dict['ENGINE']:
                cursor.execute(f"ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1;")
                retorno = "Autoincremento resetado (PostgreSQL)."
                msg = 'SKUs deletados e IDs resetados com sucesso.'

            elif 'mysql' in connection.settings_dict['ENGINE']:
                cursor.execute(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1;")
                retorno = "Autoincremento resetado (MySQL)."
                msg = 'SKUs deletados e IDs resetados com sucesso.'
            else:
                retorno = "Banco não suportado para resetar autoincremento."
                msg = ''
    
    
            return retorno + ' - ' + msg





        