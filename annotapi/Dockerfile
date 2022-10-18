FROM python:3.11-rc-alpine AS base

RUN apk add vim git python3-dev openssh bash git g++ gcc

RUN mkdir /home/app
WORKDIR /home/app

COPY Pipfile .
COPY Pipfile.lock .
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install

COPY app/ .

EXPOSE 30193
# Points to the current dir as our app factory for flask
ENV FLASK_APP /home/app/src/app.py
# Add current dir to PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/home/app"
ENV PYTHONUNBUFFERED 1
ENTRYPOINT pipenv run flask run --host=0.0.0.0 --port=30193
