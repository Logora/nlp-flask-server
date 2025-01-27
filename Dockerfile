FROM python:3.9-slim

RUN apt-get update && apt-get install -y \ 
    libpq-dev \
    build-essential \ 
    git

COPY requirements.txt /

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 8000

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000", "--chdir", "app/", "-w", "1", "--threads", "4"]
