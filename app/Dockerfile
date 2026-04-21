FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar ddtrace para APM
RUN pip install --no-cache-dir ddtrace

COPY . .

# Crear directorio static para demo de path traversal
RUN mkdir -p /app/static && echo "archivo de prueba" > /app/static/demo.txt

EXPOSE 8080

# Arrancar con ddtrace para APM automático
CMD ["ddtrace-run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
