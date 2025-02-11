FROM python:slim-bullseye
WORKDIR /app
COPY app/requirements.txt .
RUN pip install -r requirements.txt 
COPY app /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
