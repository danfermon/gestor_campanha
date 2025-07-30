import json
import sqlite3
import psycopg2
from psycopg2 import sql
import os

# CONFIGURAÇÃO
JSON_PATH = 'dados.json'
MODO = 'postgres'  # 'sqlite' ou 'postgres'

# Config Postgres
POSTGRES_CONFIG = {
    'dbname': 'railway',
    'user': 'postgres',
    'password': 'VYpFBDbdnPTmEunfDnrzgrlFMMXwJVuy',
    'host': 'yamanote.proxy.rlwy.net',
    'port': 37607,
}

# FUNÇÃO PARA PARSEAR LINHA EX: "nome;ean;dun;categoria"
def parse_linha(linha: str):
    partes = linha.split(';')
    if len(partes) == 4:
        return {
            'nome': partes[0].strip(),
            'ean': partes[1].strip(),
            'dun': partes[2].strip(),
            'categoria': partes[3].strip()
        }
    return None

# Lê e transforma o JSON
def carregar_dados(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        bruto = json.load(f)

    registros = []

    for item in bruto:
        if "Nome;Ean;Dun;Categoria" in item:
            principal = parse_linha(item["Nome;Ean;Dun;Categoria"])
            if principal:
                registros.append(principal)

        if "null" in item:
            for sublinha in item["null"]:
                secundario = parse_linha(sublinha)
                if secundario:
                    registros.append(secundario)
    return registros

# SQLite
def salvar_sqlite(dados):
    conn = sqlite3.connect('produtos.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            ean TEXT,
            dun TEXT,
            categoria TEXT
        )
    ''')

    for d in dados:
        cur.execute('''
            INSERT INTO produtos (nome, ean, dun, categoria)
            VALUES (?, ?, ?, ?)
        ''', (d['nome'], d['ean'], d['dun'], d['categoria']))

    conn.commit()
    conn.close()
    print('✅ Dados inseridos no SQLite!')

# PostgreSQL
def salvar_postgres(dados):
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id SERIAL PRIMARY KEY,
            nome TEXT,
            ean TEXT,
            dun TEXT,
            categoria TEXT
        )
    ''')

    for d in dados:
        cur.execute('''
            INSERT INTO produtos (nome, ean, dun, categoria)
            VALUES (%s, %s, %s, %s)
        ''', (d['nome'], d['ean'], d['dun'], d['categoria']))

    conn.commit()
    cur.close()
    conn.close()
    print('✅ Dados inseridos no PostgreSQL!')

# EXECUÇÃO
if __name__ == '__main__':
    dados = carregar_dados(JSON_PATH)

    if MODO == 'sqlite':
        salvar_sqlite(dados)
    elif MODO == 'postgres':
        salvar_postgres(dados)
    else:
        print("❌ MODO inválido. Use 'sqlite' ou 'postgres'.")
