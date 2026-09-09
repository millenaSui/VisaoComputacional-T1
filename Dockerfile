FROM python:3.10-slim

WORKDIR /app

# instala dependências do sistema exigidas pelo OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# copia e instala as dependências do python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copia o restante do projeto para dentro do container
COPY . .

# executa o script principal
CMD ["python", "main.py"]