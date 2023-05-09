FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip

RUN apt-get update && apt-get -y upgrade && apt-get install -y \
    python3-pip \
    libmariadb-dev-compat

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000