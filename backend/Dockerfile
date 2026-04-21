FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/static && echo "workshop demo file" > /app/static/demo.txt

EXPOSE 8000

ENV DD_SERVICE=dd-workshop-api
ENV DD_ENV=workshop
ENV DD_VERSION=2.0.0
ENV DD_LOGS_INJECTION=true
ENV DD_TRACE_SAMPLE_RATE=1.0
ENV DD_PROFILING_ENABLED=true

CMD ["ddtrace-run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
