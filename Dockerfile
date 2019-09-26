FROM python:3.6-alpine
RUN pip3 install poetry
RUN mkdir /tmp/app
WORKDIR /tmp/app

