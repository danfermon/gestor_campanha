### FUNÇÕES PARA A VALIDAÇÃO DE CUPONS DE CONSUMIDOR E NOTAS FISCAIS
import requests
import json
import os
import re

def extrair_texto_ocr(imagem_path):
    """
    Recebe o caminho da imagem e retorna o texto extraído via OCR.
    """
    try:
        imagem = Image.open(imagem_path)
        texto = pytesseract.image_to_string(imagem, lang="por")
        return texto
    except Exception as e:
        print(f"Erro ao processar OCR: {e}")
        return f"Erro ao processar OCR: {e}"



def parse_dados_cupom(texto):
    """Extrai dados estruturados do conteúdo OCR do QR Code (modelo SAT SP)."""
    dados = {}

    # CNPJ
    cnpj_match = re.search(r'CNPJ\s*[:\-]?\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', texto)
    if cnpj_match:
        dados['cnpj'] = cnpj_match.group(1)

    # Data e hora
    data_match = re.search(r'Data[:\-]?\s*(\d{2}/\d{2}/\d{4})', texto)
    hora_match = re.search(r'(\d{2}:\d{2}:\d{2})', texto)
    if data_match:
        dados['data'] = data_match.group(1)
    if hora_match:
        dados['hora'] = hora_match.group(1)

    # Valor total
    total_match = re.search(r'Total[:\-]?\s*R?\$?\s*([0-9,.]+)', texto, re.IGNORECASE)
    if total_match:
        dados['total'] = total_match.group(1)

    # Número SAT
    sat_match = re.search(r'SAT[:\-]?\s*(\d+)', texto)
    if sat_match:
        dados['sat'] = sat_match.group(1)

    # Chave QR (44 dígitos)
    chave_match = re.search(r'\b(\d{44})\b', texto)
    if chave_match:
        dados['chave_qr'] = chave_match.group(1)

    return dados



def extrair_numero_cupom(texto):
    """
    Extrai a chave de acesso (44 dígitos) do cupom fiscal a partir de OCR ou QR Code.
    """
    match = re.search(r'\b\d{44}\b', texto)
    return match.group() if match else ''

def consulta_sefaz(url):
    dados_cupom = requests.POST(url)

    if dados_cupom.status_code == 200:
        print(dados_cupom.json())
        return dados_cupom.json()
    else:
        print(dados_cupom.status_code)
        return dados_cupom.status_code


# função para verificar se produtos em cupom enviado estão validos na campanha
def validar_produto(lista_produtos_cupom):
    for i in lista_produtos_cupom:
        if i == '':
            retorno = 'ok'


# extrair produtos do cupom
def extrair_produtos(cupom):
    ...