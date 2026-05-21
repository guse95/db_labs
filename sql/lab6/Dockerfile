FROM python:3.13-alpine

WORKDIR /usr/sql/lab6/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /usr/sql/lab6/app/requirements.txt

RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        libressl-dev libffi-dev gcc musl-dev python3-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /usr/sql/lab6/app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /usr/sql/lab6/app/