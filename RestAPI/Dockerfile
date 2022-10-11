FROM python:3.11-rc-slim AS base

RUN mkdir /home/app
RUN mkdir /home/collections
WORKDIR /home/app

COPY Pipfile .
COPY Pipfile.lock .
COPY core/ ./core
COPY api/ .

# Necessary libraries to build psycopg2
RUN apt update && apt upgrade
RUN apt add postgresql-dev gcc python3-dev musl-dev
RUN apt add --no-cache bash git openssh
RUN apt add --update --no-cache g++ gcc libxslt-dev
RUN apt add libxml2
RUN apt add libjpeg
RUN apt --update add libffi-dev musl-dev libgcc openssl-dev curl
RUN apt add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
RUN apt add vim tmux

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install
RUN pipenv install ipython

EXPOSE 5000
# Points to the current dir as our app factory for flask
ENV FLASK_APP /home/app/src/app.py
# Add current dir to PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/home/app"
ENV PYTHONUNBUFFERED 1
ENTRYPOINT pipenv run flask run --host=0.0.0.0 --port=5000