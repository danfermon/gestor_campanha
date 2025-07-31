FROM python:3.12-slim

# Instala libGL para o OpenCV funcionar
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

# Cria diretório da app
WORKDIR /app

# Instala dependências do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto
COPY . .

# Comando para iniciar o Django (ajuste conforme necessário)
CMD ["gunicorn", "gestor_campanhax.wsgi:application", "--bind", "0.0.0.0:$PORT"]
