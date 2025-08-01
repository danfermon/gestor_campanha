## teste com api free que retorna dados de cupom do consumidor, informado o gtin da nota

import requests

def get_token():
  url = "https://gtin.rscsistemas.com.br/oauth/token"

  headers = {
      "username": "Danatielly",
      "password": "##Adarg12##",
      "Authorization": "Basic RGFubnk6IyNBZGFyZzEyIyM=",
      "User-Agent": "PostmanRuntime/7.38.0",  # Simulando o Postman
      "Accept": "*/*",                       # Postman envia isso
      "Cache-Control": "no-cache",          # Opcional
      "Connection": "keep-alive"            # Opcional
  }

  response = requests.post(url, headers=headers)
  print("Status:", response.status_code)
  print("Resposta:", response.text)
  

def consulta_gtin(gtin, token):
  url = f'https://gtin.rscsistemas.com.br/api/gtin/infor/:{gtin}'

  payload = {
    "token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjU2NSwiZXhwIjoxNzUyODY0ODEwLCJpYXQiOjE3NTI4NjEyMTB9.vpxqOlD_I7xl7ZDXfoukhSzMOsAocdSxnFjwoku6Z0M"     
  }

  response = requests.get(url, data=payload)
  print("Status:", response.status_code)
  print("Resposta:", response.text)

#get_token()


# Token que você obteve
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjU2NSwiZXhwIjoxNzUyODY0ODEwLCJpYXQiOjE3NTI4NjEyMTB9.vpxqOlD_I7xl7ZDXfoukhSzMOsAocdSxnFjwoku6Z0M"

# GTIN a ser consultado
gtin = "789102286160"

# Endpoint
url = f"https://gtin.rscsistemas.com.br/api/gtin/infor/{gtin}"

# Headers copiados do padrão que funcionou antes
headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "*/*",
    "User-Agent": "PostmanRuntime/7.38.0",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive"
}

# Faz a requisição
response = requests.get(url, headers=headers)

# Exibe o resultado
print("Status:", response.status_code)
print("Resposta:", response.text)

