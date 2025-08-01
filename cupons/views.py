import os
import uuid
import json
import numpy as np

from django.shortcuts import render, get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from cupons.models import Cupom
from participantes.models import Participantes
from utils.funcoes_cupom import extrair_texto_ocr, extrair_numero_cupom, parse_dados_cupom
from utils.api_sefaz import consulta_api_sefaz

import cv2


def guardar_cupom(arquivo):
    """Salva a imagem do cupom no storage padrão e retorna o caminho salvo."""
    ext = os.path.splitext(arquivo.name)[1]
    nome_arquivo = f"{uuid.uuid4()}{ext}"
    caminho_arquivo = os.path.join('cupons', nome_arquivo)
    return default_storage.save(caminho_arquivo, ContentFile(arquivo.read()))


def gerar_link_sefaz(chave):
    """
    Gera o link de consulta da chave na SEFAZ-SP.
    Pode ser adaptado para outro estado se necessário.
    """
    return f"https://www.sefaz.sp.gov.br/NFCeConsultaPublica/consultarNFCe?chNFe={chave}"





## CADASTRAR CUPOM PELO CÓDIGO
def cad_cupom_codigo(request, id_participante):
    if request.method == 'POST':
        # verifica se o post foi por formulário
        cod_cupom = request.POST.get('cod_cupom')

        print(cod_cupom)

        participante = get_object_or_404(Participantes, id=id_participante)
        # fazer a consulta no sefaz
        retorno_sefaz = json.dumps(consulta_api_sefaz(cod_cupom))
        # Cria cupom no banco
        Cupom.objects.create(
            participante=participante,
            dados_cupom=retorno_sefaz,
            tipo_envio='Sistema',
            status='Pendente',
            numero_documento=cod_cupom,
            dados_json= retorno_sefaz
        )
        
        msg = 'Cupom enviado com sucesso!'
        qr_msg = 'Cupom inserido via Código Fiscal'
        id_participante = id_participante
        return render(request, 'cad_cupom.html', {
        'msg': msg,
        'qr_msg': qr_msg,
        'id_participante': id_participante,})
       

# cadastro de cupom por qrcode e imagem
def cad_cupom(request, id_participante):
    """View para cadastro do cupom via upload de imagem e processamento OCR + QR Code."""
    """ E também via formulário com codigo de cupom fiscal"""
    msg = ''
    qr_msg = ''

    if request.method == 'POST':
        arquivo = request.FILES.get('img_cupom')

        if not arquivo:
            msg = 'Selecione um arquivo no formato de imagem.'
        else:
            try:
                # Salva a imagem no storage configurado
                path = guardar_cupom(arquivo)
                # Abre a imagem como array para OpenCV
                with default_storage.open(path, 'rb') as f:
                    file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
                    imagem_cv = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                if imagem_cv is None:
                    raise ValueError("Imagem não pôde ser carregada.")
                # Detecta QR Code na imagem (se existir)
                gray = cv2.cvtColor(imagem_cv, cv2.COLOR_BGR2GRAY)
                detector = cv2.QRCodeDetector()
                dados_qr, _, _ = detector.detectAndDecode(gray)
                # Extrai texto via OCR (função personalizada)
                imagem_local_path = default_storage.path(path)
                dados_ocr = extrair_texto_ocr(imagem_local_path)
                # Tenta extrair a chave de acesso (44 dígitos) do QR Code ou OCR
                chave_acesso = extrair_numero_cupom(dados_qr or dados_ocr)
                link_sefaz = gerar_link_sefaz(chave_acesso) if chave_acesso else ''
                print('Chave: :' + chave_acesso + ' Link sefaz: ' + link_sefaz)
                # fazer a consulta no sefaz
                retorno_sefaz = consulta_api_sefaz(chave_acesso)
                # Busca participante no banco
                participante = get_object_or_404(Participantes, id=id_participante)
                # Cria cupom no banco
                Cupom.objects.create(
                    participante=participante,
                    imagem_cupom=path,
                    ocr_text=dados_ocr.strip(),
                    dados_cupom=retorno_sefaz,
                    tipo_envio='Sistema',
                    status='Pendente',
                    numero_documento=chave_acesso,
                    link_consulta=link_sefaz,
                    dados_json=retorno_sefaz
                )
                qr_msg = f"QR Code detectado: {dados_qr}" if dados_qr else "Nenhum QR Code detectado."
                msg = 'Cupom enviado com sucesso!'
            except Participantes.DoesNotExist:
                msg = 'Participante não encontrado.'
            except Exception as e:
                print(f"[ERRO] {e}")
                msg = 'Erro ao processar o cupom.'

    return render(request, 'cad_cupom.html', {
        'msg': msg,
        'qr_msg': qr_msg,
        'id_participante': id_participante,
    })


@csrf_exempt
def salvar_qrcode_ajax(request, id_participante):
    """Recebe dados QR Code via AJAX (JSON) e cria cupom vinculado ao participante."""
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            dados_qr = body.get('dados_qr')

            if not dados_qr:
                return JsonResponse({'status': 'erro', 'mensagem': 'QR Code vazio.'})

            participante = get_object_or_404(Participantes, id=id_participante)

            Cupom.objects.create(
                participante=participante,
                imagem_cupom=None,
                dados_cupom=dados_qr,
                tipo_envio='QR-Câmera',
                status='Pendente',
            )

            return JsonResponse({'status': 'ok', 'mensagem': 'QR Code salvo com sucesso!'})

        except Participantes.DoesNotExist:
            return JsonResponse({'status': 'erro', 'mensagem': 'Participante não encontrado.'})
        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)})

    return JsonResponse({'status': 'erro', 'mensagem': 'Método inválido'})





def cad_produtos(produto):
    ...