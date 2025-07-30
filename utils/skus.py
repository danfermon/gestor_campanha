import csv
import json

def csv_to_json(csv_filepath, json_filepath):
    """
    Converte um arquivo CSV em JSON.

    Args:
        csv_filepath (str): Caminho para o arquivo CSV de entrada.
        json_filepath (str): Caminho para o arquivo JSON de saída.
    """
    data = []
    with open(csv_filepath, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            data.append(row)

    with open(json_filepath, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)

# Exemplo de uso:
csv_file = 'lista_exportada.csv'  # Substitua pelo nome do seu arquivo CSV
json_file = 'dados.json' # Substitua pelo nome desejado para o arquivo JSON
csv_to_json(csv_file, json_file)

print(f"Arquivo CSV '{csv_file}' convertido para JSON '{json_file}'")