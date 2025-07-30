import cv2
import os
import matplotlib.pyplot as plt

# Caminho da imagem
path = 'cupo qrCode.jpg'

# Verifica se o arquivo existe
if not os.path.exists(path):
    print("Imagem não encontrada.")
    exit()

# Lê a imagem
img = cv2.imread(path)

# Verifica se foi lida corretamente
if img is None:
    print("Erro ao carregar a imagem.")
    exit()

# Converte para escala de cinza
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Converte para PB com threshold de Otsu
_, pb = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Inicializa o detector
detector = cv2.QRCodeDetector()

# Tenta detectar na imagem PB
data, bbox, _ = detector.detectAndDecode(pb)

# Mostra resultado
if bbox is not None and data:
    print("[+] QR Code detectado:", data)
    for i in range(len(bbox)):
        cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), (0, 255, 0), 2)
else:
    print("[-] Nenhum QR Code detectado.")

# Mostra imagem com matplotlib (evita erro do Qt em Linux headless)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Imagem do Cupom")
plt.axis("off")
plt.show()
