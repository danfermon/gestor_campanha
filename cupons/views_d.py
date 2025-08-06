import os
import uuid
import json
from venv import logger
import numpy as np
import cv2

from django.shortcuts import render, get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required # Recomendado

from .models import Cupom
from participantes.models import Participantes
from utils.funcoes_cupom import extrair_texto_ocr, extrair_numero_cupom
from utils.api_sefaz import consulta_api_sefaz
from utils.link_sefaz import gerar_link_sefaz # Movido para um local mais apropriado

def guardar_cupom(arquivo):
    """Salva a imagem do cupom no storage padrão e retorna o caminho salvo."""
    ext = os.path.splitext(arquivo.name)[1]
    nome_arquivo = f"cupom_{uuid.uuid4().hex}{ext}"
    caminho_arquivo = os.path.join('cupons', nome_arquivo)
    return default_storage.save(caminho_arquivo, ContentFile(arquivo.read()))

# @login_required # É uma boa prática proteger views que modificam dados
def cadastrar_cupom(request, id_participante):
    """
    View unificada para cadastro de cupom via upload de imagem ou código digitado.
    """
    contexto = {'id_participante': id_participante}
    participante = get_object_or_404(Participantes, id=id_participante)

    if request.method == 'POST':
        chave_acesso = None
        imagem_path = None
        dados_ocr = ""

        # Rota 1: Formulário de envio de imagem
        if 'submit_imagem' in request.POST:
            arquivo = request.FILES.get('img_cupom')
            if not arquivo:
                contexto['msg_erro'] = 'Nenhum arquivo de imagem foi selecionado.'
            else:
                try:
                    imagem_path = guardar_cupom(arquivo)
                    imagem_local_path = default_storage.path(imagem_path)

                    # Processamento de Imagem (OCR e QR Code)
                    imagem_cv = cv2.imread(imagem_local_path)
                    if imagem_cv is None:
                        raise ValueError("Não foi possível carregar a imagem para processamento.")
                    
                    gray = cv2.cvtColor(imagem_cv, cv2.COLOR_BGR2GRAY)
                    detector = cv2.QRCodeDetector()
                    dados_qr, _, _ = detector.detectAndDecode(gray)
                    
                    dados_ocr = extrair_texto_ocr(imagem_local_path)
                    chave_acesso = extrair_numero_cupom(dados_qr or dados_ocr)

                except Exception as e:
                    contexto['msg_erro'] = f'Erro ao processar a imagem: {e}'
        
        # Rota 2: Formulário de envio de código
        elif 'submit_codigo' in request.POST:
            chave_acesso = request.POST.get('cod_cupom')

        # Processamento da Chave de Acesso (comum a ambas as rotas)
        if chave_acesso:
            if len(chave_acesso) != 44:
                contexto['msg_erro'] = 'O código do cupom extraído ou digitado é inválido.'
            else:
                dados_sefaz = consulta_api_sefaz(chave_acesso)
                if dados_sefaz:
                    Cupom.objects.create(
                        participante=participante,
                        imagem_cupom=imagem_path,
                        ocr_text=dados_ocr.strip(),
                        dados_json=dados_sefaz,
                        tipo_envio='Imagem' if imagem_path else 'Sistema',
                        status='Aprovado', # Ou 'Pendente' se houver moderação
                        numero_documento=chave_acesso,
                        link_consulta=gerar_link_sefaz(chave_acesso)
                    )
                    contexto['msg_sucesso'] = 'Cupom cadastrado com sucesso!'
                else:
                    contexto['msg_erro'] = 'Não foi possível validar o cupom. Verifique os dados ou tente novamente.'
        elif 'submit_imagem' in request.POST and not contexto.get('msg_erro'):
             contexto['msg_erro'] = 'Não foi possível encontrar um código de cupom na imagem enviada.'

    return render(request, 'cad_cupom.html', contexto)


@csrf_exempt
# @login_required
def salvar_qrcode_ajax(request, id_participante):
    """Recebe dados do QR Code lido pela câmera via AJAX e tenta registrar o cupom."""
    if request.method != 'POST':
        return JsonResponse({'status': 'erro', 'mensagem': 'Método inválido.'}, status=405)

    try:
        body = json.loads(request.body)
        dados_qr = body.get('dados_qr')
        
        if not dados_qr:
            return JsonResponse({'status': 'erro', 'mensagem': 'Nenhum dado de QR Code recebido.'}, status=400)

        chave_acesso = extrair_numero_cupom(dados_qr)
        if not chave_acesso or len(chave_acesso) != 44:
            return JsonResponse({'status': 'erro', 'mensagem': 'Não foi possível extrair uma chave válida do QR Code.'}, status=400)

        participante = get_object_or_404(Participantes, id=id_participante)
        dados_sefaz = consulta_api_sefaz(chave_acesso)

        if dados_sefaz:
            Cupom.objects.create(
                participante=participante,
                dados_json=dados_sefaz,
                tipo_envio='QR-Câmera',
                status='Aprovado',
                numero_documento=chave_acesso,
                link_consulta=gerar_link_sefaz(chave_acesso)
            )
            return JsonResponse({'status': 'ok', 'mensagem': 'Cupom validado e salvo com sucesso!'})
        else:
            return JsonResponse({'status': 'erro', 'mensagem': 'Cupom inválido ou não encontrado na Sefaz.'}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'status': 'erro', 'mensagem': 'Requisição JSON malformada.'}, status=400)
    except Participantes.DoesNotExist:
        return JsonResponse({'status': 'erro', 'mensagem': 'Participante não encontrado.'}, status=404)
    except Exception as e:
        # Logar o erro real no servidor é importante
        logger.error(f"Erro inesperado em salvar_qrcode_ajax: {e}")
        return JsonResponse({'status': 'erro', 'mensagem': 'Ocorreu um erro interno.'}, status=500)