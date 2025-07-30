import cv2

path = 'cupo qrCode.jpg'
img = cv2.imread(path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Converte em preto e branco com Otsu
_, pb = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Usa o PB no QRCodeDetector
data, bbox, _ = detector.detectAndDecode(pb)
