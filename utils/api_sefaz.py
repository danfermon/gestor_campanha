# Testado com Python 3.13.5
import requests

def consulta_api_sefaz(chave):

  url = 'https://api.infosimples.com/api/v2/consultas/sefaz/sp/cfe'
  args = {
    "chave":  chave, #"35250501157555004100590004797948322835671276",
    "token":   "VhGk5q69irbXv6baG7HVKy__qlh_AhFBzvVSRweX",
    "timeout": 300
  }

  response = requests.post(url, args)
  response_json = response.json()
  response.close()

  if response_json['code'] == 200:
    print("Retorno com sucesso: ", response_json['data'])

  elif response_json['code'] in range(600, 799):
    mensagem = "Resultado sem sucesso. Leia para saber mais: \n"
    mensagem += "Código: {} ({})\n".format(response_json['code'], response_json['code_message'])
    mensagem += "; ".join(response_json['errors'])
    print(mensagem)

  print("Cabeçalho da consulta: ", response_json['header'])
  print("URLs com arquivos de visualização (HTML/PDF): ", response_json['site_receipts']) 

  return response_json