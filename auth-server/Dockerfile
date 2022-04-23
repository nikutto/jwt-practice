FROM python:3.8.13-alpine3.15

RUN mkdir app
WORKDIR /app

# Create pipenv
RUN python -m pip install pipenv
COPY Pipfile .
RUN pipenv install

COPY . .

CMD pipenv run uvicorn app.main:app --port 8000 --host 0.0.0.0
