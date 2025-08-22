FROM python:3.13.2

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /hw

COPY requirements.txt /hw/requirements.txt

RUN pip install -r /hw/requirements.txt

COPY . .