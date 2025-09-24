FROM python:3.12-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

COPY . /app