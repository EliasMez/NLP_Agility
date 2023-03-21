FROM python:3.10-slim

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY . /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt &&\
    python load_model.py


EXPOSE 80

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--workers", "4", "--port", "80", "--timeout-keep-alive", "600" ]