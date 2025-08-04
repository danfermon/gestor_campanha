import requests

# URL da API
url = "http://127.0.0.1:8000/api/participantes/"

# Seu token gerado no admin
token = "token_usuario"  # Substitua pelo token real

# Cabeçalho com o token
headers = {
    "Authorization": f"Token {token}"
}

# Requisição GET para listar os participantes
response = requests.get(url, headers=headers)

# Mostrar o resultado
print(f"Status: {response.status_code}")
print("Resposta:")
print(response.json())
