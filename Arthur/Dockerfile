FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

# Install Requirements
RUN pip install pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --system
RUN python -m nltk.downloader punkt
COPY . /code/


