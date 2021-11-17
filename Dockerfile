FROM python:3.8-slim

ENV PYTHONUNBUFFERED True
ENV APP_HOME/app
WORKDIR $APP_HOME

COPY . ./
RUN pip install -r requirements.txt
RUN pip install Flask guicorn


CMD exec guicorn --bind :$PORT --workers 1 --threads 9 --timeout 0 app:app