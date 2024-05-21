FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 1026

CMD ["python", "-u", "serv.py"]
