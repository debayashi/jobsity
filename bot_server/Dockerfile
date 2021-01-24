
FROM python:3-alpine

RUN apk add build-base libffi-dev bash

USER root

WORKDIR /server

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR /

CMD ["/bin/bash", "-c", "python3 -m bot_server"]