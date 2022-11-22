FROM python:3.10.8-alpine AS base

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
#ENV FLASK_APP /home/app/server.py
# Add current dir to PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/home/app"
ENV PYTHONUNBUFFERED 1

ENTRYPOINT pipenv run python /home/app/build_database.py --no-reset && pipenv run python /home/app/server.py
