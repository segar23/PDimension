FROM python:3.8.2-slim-buster

RUN apt-get update -y && \
    apt-get install gcc -y && \
    apt-get clean && \
    mkdir /var/www

WORKDIR /var/www
ADD . .

RUN pip install -r requirements.txt && \
    python manage.py migrate && \
    chown -R www-data. /var/www

RUN pip install https://projects.unbit.it/downloads/uwsgi-lts.tar.gz

EXPOSE 8000
USER www-data
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
