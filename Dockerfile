FROM python:slim-bullseye
RUN apt install xvfb libfontconfig wkhtmltopdf -y --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY app/requirements.txt .
RUN pip install -r requirements.txt 
COPY app /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
