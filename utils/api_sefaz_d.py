import requests
import logging
from django.conf import settings

# Configura um logger para este módulo.
# As mensagens de log aparecerão no console do Django.
logger = logging.getLogger(__name__)

def consulta_api_sefaz(chave: str) -> dict | None:
    """
    Consulta a chave de um cupom fiscal na API do InfoSimples.

    Esta função encapsula a chamada à API, tratando a autenticação,
    a formatação da requisição e os possíveis erros de comunicação ou da API.

    Args:
        chave: A chave de 44 dígitos do cupom fiscal.

    Returns:
        Um dicionário com os dados da consulta em caso de sucesso.
        Retorna None em caso de qualquer falha (configuração, comunicação, erro da API).
    """
    try:
        api_key = settings.API_KEY_SEFAZ
        if not api_key:
            logger.error("A variável API_KEY_SEFAZ não está configurada nas settings do Django.")
            return None
    except AttributeError:
        logger.error("API_KEY_SEFAZ não foi encontrada nas settings. Verifique seu .env e settings.py.")
        return None

    # Endpoint para consulta de CF-e de São Paulo.
    # Pode ser tornado dinâmico no futuro para suportar outros estados.
    url = 'https://api.infosimples.com/consultas/docs/sefaz/sp/cfe'
    
    payload = {
        "chave": chave,
        "token": api_key,
        "timeout": 60  # Timeout de 60 segundos para a consulta.
    }

    try:
        # Realiza a requisição POST para a API.
        response = requests.post(url, json=payload, timeout=60)

        
        response.raise_for_status()

        response_data = response.json()

        # VERIFICAÇÃO do código de sucesso da lógica interna do InfoSimples.
        if response_data.get('code') == 200:
            logger.info(f"Consulta à Sefaz bem-sucedida para a chave iniciando com {chave[:10]}...")
            # Retorna apenas o payload de dados.
            return response_data.get('data')
        else:
            error_message = response_data.get('errors', ['Erro desconhecido retornado pela API.'])
            #logger.error(f"Erro da API InfoSimples ao consultar chave iniciando com {chave[:10]...}: {'; '.join(error_message)}")
            logger.error(
                f"Erro da API InfoSimples ao consultar chave iniciando com {chave[:10]}...: {'; '.join(error_message)}"
            )

            return None

    except requests.exceptions.Timeout:
        logger.error("Erro de comunicação: A requisição para a API da Sefaz expirou (timeout).")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro de comunicação ao consultar a API da Sefaz: {e}")
        return None
    except ValueError: # Erro na decodificação do JSON
        logger.error("Erro de decodificação: A resposta da API da Sefaz não é um JSON válido.")
        return None