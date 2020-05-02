# PDimension

to build the Docker image:
`docker build . -t magic:0.1`

to run the container:
`docker run -p 8000:8000 magic:0.1`

For production desployment, uwsgi is a recommended server. Ex:
`uwsgi --socket 127.0.0.1:3031 --chdir /var/www --wsgi-file PDimension/wsgi.py --master --processes 2 --threads 2 --stats 0.0.0.0:8000`