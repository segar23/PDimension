# PDimension

to build the Docker image for testing:
`docker build . -t magic_test:latest`

to run the container:
`docker run -p 8000:8000 magic_test:latest`

Production deployment:
in the django directory, run:
`docker build -f ../uwsgi/Dockerfile . -t agic:latest`
in the nginx directory:
`docker build . -t nginx_magic:latest`

Test the stack:
in the project root, run:
`docker-compose up`