# utils/api_sefaz.py

import requests
import logging
from django.conf import settings

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
        Retorna None em caso de qualquer falha.
    """
    try:
        api_key = settings.API_KEY_SEFAZ
        if not api_key:
            logger.error("A variável API_KEY_SEFAZ não está configurada nas settings do Django.")
            return None
    except AttributeError:
        logger.error("API_KEY_SEFAZ não foi encontrada nas settings. Verifique seu .env e settings.py.")
        return None

    url = 'https://api.infosimples.com/api/v2/consultas/sefaz/sp/cfe'
    
    payload = {
        "chave": chave,
        "token": api_key,
        "timeout": 60
    }

    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        response_data = response.json()

        if response_data.get('code') == 200:
            logger.info(f"Consulta à Sefaz bem-sucedida para a chave iniciando com {chave[:10]}...")
            return response_data.get('data')
        else:
            # Pega a mensagem de erro da API.
            api_errors = response_data.get('errors')
            
            # Verifica o tipo da mensagem de erro para tratá-la corretamente.
            if isinstance(api_errors, list):
                # Se for uma lista, une os elementos.
                error_message_str = '; '.join(str(e) for e in api_errors)
            elif api_errors:
                # Se não for lista mas existir (ex: uma string), usa diretamente.
                error_message_str = str(api_errors)
            else:
                # Se não houver mensagem, usa um valor padrão.
                error_message_str = 'Erro desconhecido retornado pela API.'

            logger.error(
                f"Erro da API InfoSimples ao consultar chave iniciando com {chave[:10]}...: {error_message_str}"
            )
        
            return None

    except requests.exceptions.Timeout:
        logger.error(f"Erro de comunicação: A requisição para a API da Sefaz (chave {chave[:10]}...) expirou.")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro de comunicação ao consultar a API da Sefaz (chave {chave[:10]}...): {e}")
        return None
    except ValueError:
        logger.error(f"Erro de decodificação: A resposta da API da Sefaz (chave {chave[:10]}...) não é um JSON válido.")
        return None