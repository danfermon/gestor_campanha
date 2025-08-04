import requests

url = " http://127.0.0.1:8000/api/participantes/buscar-por-celular/"
token = "58f9bd5cb1206768314996da54729462720bafa6"

headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
}

payload = {
    "celular": "(11) 97584-4549"
}

response = requests.post(url, headers=headers, json=payload)

print(f"Status: {response.status_code}")
print(response.json())
