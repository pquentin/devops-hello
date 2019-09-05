FROM python:3.7-alpine

RUN apk update && apk add nginx

ENV prometheus_multiproc_dir /tmp
ADD . /opt/app
WORKDIR /opt/app

RUN pip install pipenv
RUN pipenv install --deploy
RUN pipenv run pytest hello.py

CMD pipenv run supervisord -c /opt/app/supervisord.conf
