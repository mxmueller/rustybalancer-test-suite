# Verwende ein offizielles Python-Runtime-Image als Basis
FROM --platform=$BUILDPLATFORM python:3.9-slim

# Setze Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die Projektdateien in das Arbeitsverzeichnis
COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install fastapi uvicorn

# Installiere die Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Mache Port 8080 verfügbar für die Welt außerhalb des Containers
EXPOSE 8080

# Definiere Umgebungsvariable
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["uvicorn", "main:app", "--host" , "0.0.0.0", "--port", "8080"]
# Starte die Anwendung
CMD ["python", "app.py"]
