FROM python:3.12

ENV LIBRARY_PATH=/app:/lib:/usr/lib
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && apt-get clean

RUN pip install --upgrade setuptools


ADD code /app/

WORKDIR  /app/

RUN pip install --disable-pip-version-check --no-python-version-warning --no-cache-dir --retries 2 --timeout 5 -r requirements.txt
