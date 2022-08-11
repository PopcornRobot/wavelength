# pull official base image
FROM python:3.10.2-alpine

# set work directory
WORKDIR /app

# set environment variables

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1
# 0 is production, 1 is debug mode
ENV DEBUG 1

# install psycopg2
RUN apk update \
    && apk add --virtual build-essential gcc python3-dev musl-dev \
    && apk add --no-cache libffi-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# collect static files
# RUN python manage.py collectstatic --noinput -i admin -i django_extensions -i debug_toolbar

# add and run as non-root user
RUN adduser -D myuser
USER myuser

# run gunicorn
CMD gunicorn wavelength.wsgi:application --bind 0.0.0.0:$PORT
