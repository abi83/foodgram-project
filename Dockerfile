FROM python:3.8.5
LABEL author='Wladimir Kromm' version=1.0


WORKDIR /code

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY . /code

ARG DJANGO_ENV=prod_settings
ENV DJANGO_SETTINGS_MODULE=foodgram.${DJANGO_ENV}
