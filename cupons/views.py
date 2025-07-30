import os
import uuid

from django.shortcuts import render, get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from cupons.models import Cupom
from participantes.models import Participantes

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import cv2
import numpy as np
from utils.funcoes import extrair_texto_ocr


def cad_produto(request):
    return render(request, 'cad_produto.html')  


def guardar_cupom(arquivo):
    ext = os.path.splitext(arquivo.name)[1]
    nome_arquivo = f"{uuid.uuid4()}{ext}"
    caminho_arquivo = os.path.join('cupons', nome_arquivo)
    return default_storage.save(caminho_arquivo, ContentFile(arquivo.read()))


def cad_cupom(request, id_participante):
    msg = ''
    qr_msg = ''

    if request.method == 'POST':
        arquivo = request.FILES.get('img_cupom')

        if not arquivo:
            msg = 'Selecione um arquivo no formato de imagem.'
        else:
            try:
                # Salva a imagem no armazenamento configurado
                path = guardar_cupom(arquivo)

                # Lê o arquivo como array do OpenCV
                with default_storage.open(path, 'rb') as f:
                    file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
                    imagem_cv = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

                if imagem_cv is None:
                    raise ValueError("Imagem não pôde ser carregada.")

                # Detecta QR Code
                gray = cv2.cvtColor(imagem_cv, cv2.COLOR_BGR2GRAY)
                detector = cv2.QRCodeDetector()
                dados_qr, _, _ = detector.detectAndDecode(gray)

                # Extrai texto via OCR (usando PIL)
                imagem_local_path = default_storage.path(path)
                dados_ocr = extrair_texto_ocr(imagem_local_path)

                # Busca o participante e cria o cupom
                participante = get_object_or_404(Participantes, id=id_participante)

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
    if request.method == "POST" and request.FILES.get("imagem_cupom"):
        imagem = request.FILES["imagem_cupom"]
        file_bytes = np.asarray(bytearray(imagem.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)

        return JsonResponse({"qr_code": data if data else None})
    return JsonResponse({"error": "Requisição inválida."}, status=400)
    

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def salvar_qrcode_ajax(request, id_participante):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            dados_qr = body.get('dados_qr')

            if not dados_qr:
                return JsonResponse({'status': 'erro', 'mensagem': 'QR Code vazio.'})

            participante = Participantes.objects.get(id=id_participante)

            Cupom.objects.create(
                participante=participante,
                imagem_cupom=None,
                dados_cupom=dados_qr,
                tipo_envio='QR-Câmera',
                status='Pendente'
            )

            return JsonResponse({'status': 'ok', 'mensagem': 'QR Code salvo com sucesso!'})

        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)})

    return JsonResponse({'status': 'erro', 'mensagem': 'Método inválido'})

#--------------------------------------------------------------------------------------------
