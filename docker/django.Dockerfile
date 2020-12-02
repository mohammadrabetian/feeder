# Pull official base image
FROM python:3.8

LABEL maintainer="Mohammad Rabetian <mohammadrabetian@gmail.com>"

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Make directory & install dependencies
RUN mkdir -p /usr/src/feeder
WORKDIR /usr/src/feeder
COPY requirements.txt /usr/src/feeder/
# RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Django sometimes raises this error and won't show the actual problem
# This line is set to resolve this issue and show the actual error
RUN sed -i "s/raise RuntimeError(\"populate() isn't reentrant\")/self.app_configs = {}/g" /usr/local/lib/python3.8/site-packages/django/apps/registry.py

# Check for dependency vulnerabilities
RUN safety check -r requirements.txt --full-report; exit 0

# Copy entrypoint file
COPY docker/django_entrypoint.sh /usr/bin/django_entrypoint.sh

# Copy project
COPY . /usr/src/feeder

ENV NAME="feeder"
ENV DJANGO_WSGI_MODULE=feeder.wsgi               
ENV DJANGO_SETTINGS_MODULE feeder.settings.development
ENV NUM_WORKERS=4  LOG_LEVEL="INFO"                      
ENV DJANGODIR /usr/src/feeder/feeder/
ENV SOCKFILE /var/run/feeder/gunicorn.sock

ENTRYPOINT ["bash", "/usr/bin/django_entrypoint.sh"]
