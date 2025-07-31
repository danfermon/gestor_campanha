import os
import uuid
import json
import numpy as np

from django.shortcuts import render, get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest

from cupons.models import Cupom
from participantes.models import Participantes

from utils.funcoes import extrair_texto_ocr

# Usando OpenCV para leitura da imagem e QR Code
import cv2


def guardar_cupom(arquivo):
    """Salva a imagem do cupom no storage padrão e retorna o caminho salvo."""
    ext = os.path.splitext(arquivo.name)[1]
    nome_arquivo = f"{uuid.uuid4()}{ext}"
    caminho_arquivo = os.path.join('cupons', nome_arquivo)
    return default_storage.save(caminho_arquivo, ContentFile(arquivo.read()))


def cad_cupom(request, id_participante):
    """View para cadastro do cupom via upload de imagem e processamento OCR + QR Code."""
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

                # Busca participante no banco
                participante = get_object_or_404(Participantes, id=id_participante)

                # Cria cupom no banco
                Cupom.objects.create(
                    participante=participante,
                    imagem_cupom=path,
                    dados_cupom=dados_ocr.strip(),
                    tipo_envio='Sistema',
                    status='Pendente'
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
def ler_qrcode_view(request):
    """API que recebe imagem via POST e retorna QR Code detectado (se houver)."""
    if request.method == "POST" and request.FILES.get("imagem_cupom"):
        try:
            imagem = request.FILES["imagem_cupom"]
            file_bytes = np.asarray(bytearray(imagem.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            detector = cv2.QRCodeDetector()
            data, bbox, _ = detector.detectAndDecode(img)

            return JsonResponse({"qr_code": data if data else None})
        except Exception as e:
            return JsonResponse({"error": f"Erro ao processar imagem: {e}"}, status=400)
    return JsonResponse({"error": "Requisição inválida."}, status=400)


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
                status='Pendente'
            )

            return JsonResponse({'status': 'ok', 'mensagem': 'QR Code salvo com sucesso!'})

        except Participantes.DoesNotExist:
            return JsonResponse({'status': 'erro', 'mensagem': 'Participante não encontrado.'})
        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)})

    return JsonResponse({'status': 'erro', 'mensagem': 'Método inválido'})


# Opcional: outras views relacionadas ao cupom podem ser adicionadas aqui

