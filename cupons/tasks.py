from celery import shared_task
from .models import Cupom
import os
import cv2
import pytesseract

@shared_task
def validar_cupons():
    from django.conf import settings
    base_dir = settings.BASE_DIR

    cupons = Cupom.objects.filter(status="Pendente")

    for cupom in cupons:
        caminho_imagem = os.path.join(base_dir, 'media', str(cupom.imagem_cupom))
        if not os.path.exists(caminho_imagem):
            continue

        imagem = cv2.imread(caminho_imagem)
        imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        _, limiarizada = cv2.threshold(imagem_cinza, 150, 255, cv2.THRESH_BINARY)
        texto = pytesseract.image_to_string(limiarizada, lang='por')

        if "CNPJ" in texto and "R$" in texto:
            cupom.status = "Validado"
            cupom.save()
