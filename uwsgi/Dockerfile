FROM python:3.8.2-slim-buster

RUN apt-get update -y && \
    apt-get install gcc -y && \
    apt-get install libpq-dev -y && \
    apt-get clean && \
    mkdir /var/www && \
    pip install https://projects.unbit.it/downloads/uwsgi-lts.tar.gz

WORKDIR /var/www
ADD . .

RUN pip install -r requirements.txt && \
    chown -R www-data. /var/www

EXPOSE 8080
USER www-data
#CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
CMD ["uwsgi", "--socket", "webapp:3031", "--chdir", "/var/www", "--wsgi-file", "PDimension/wsgi.py", "--master", "--processes", "2", "--threads", "2", "--stats", "0.0.0.0:8000"]