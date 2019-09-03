FROM python:3.7-alpine

ADD . /opt/app
WORKDIR /opt/app

RUN pip install pipenv
RUN pipenv install --deploy

ENV prometheus_multiproc_dir /tmp

RUN pipenv run pytest hello.py

CMD pipenv run gunicorn --bind 0.0.0.0 --workers 4 hello:app -c conf.py
