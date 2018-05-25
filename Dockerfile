FROM python:alpine3.7

RUN apk add --update \
    --virtual build-dependencies \
    build-base \
  && rm -rf /var/cache/apk/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

RUN apk del build-dependencies

RUN rm -rf /var/cache/apk/*

CMD python3 /usr/src/app/main.py
