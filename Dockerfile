FROM python:slim-bullseye
WORKDIR /app
COPY server/requeriments.txt .
RUN pip install -r requeriments.txt 
COPY server /app
CMD uvicorn main:app --host 0.0.0.0 --port 8000