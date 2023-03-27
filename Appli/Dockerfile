FROM python:3.10-slim

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY . /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 80

CMD ["gunicorn","--timeout", "1200","-w","4","-b","0.0.0.0:80", "app:app"]