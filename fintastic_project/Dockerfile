FROM python:3.8.1-slim-buster

ENV WORKDIR=/code
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR $WORKDIR

COPY Pipfile $WORKDIR/
RUN pip install pipenv && pipenv install --skip-lock --system --dev

COPY gunicorn /gunicorn/
COPY init /init/
COPY src $WORKDIR/
