# PDimension

to build the Docker image for testing:
`docker build . -t magic_test:latest`

to run the container:
`docker run -p 8000:8000 magic_test:latest`

development test:
`http://localhost:8000`

Production deployment:
in the django directory, run:
`docker build -f ../uwsgi/Dockerfile . -t magic:latest`

in the nginx directory:
`docker build . -t nginx_magic:latest`

"production" test url:
`http://localhost:8080`

Test the stack:
in the project root, run:
`docker-compose up`
