FROM python:3.8.13-alpine3.15

# Create pipenv
RUN python -m pip install pipenv
COPY Pipfile /app/Pipfile
WORKDIR app
RUN pipenv install

COPY . .

EXPOSE 8000
CMD ./start_server.sh
