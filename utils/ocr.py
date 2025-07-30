import os
import cv2
import pytesseract
from PIL import Image


def ocr(caminho_imagem):
    import os
    import cv2
    import pytesseract

    if not os.path.exists(caminho_imagem):
        raise FileNotFoundError(f"Imagem não encontrada: {caminho_imagem}")

    imagem = cv2.imread(caminho_imagem)
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    _, imagem_limiarizada = cv2.threshold(imagem_cinza, 150, 255, cv2.THRESH_BINARY)

    texto = pytesseract.image_to_string(imagem_limiarizada, lang='por')

    return texto


