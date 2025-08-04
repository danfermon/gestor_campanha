import requests

url = "http://127.0.0.1:8000/api/participantes/buscar-por-celular/"
token = "token_usuario"

headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
}

payload = {
    "celular": "telefone_participante"
}

response = requests.post(url, headers=headers, json=payload)

print(f"Status: {response.status_code}")
print(response.json())
