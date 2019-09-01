FROM python:3.7-alpine

ADD . /opt/app
WORKDIR /opt/app

RUN pip install -r requirements.txt

ENV prometheus_multiproc_dir /tmp

RUN pytest hello.py

CMD gunicorn --bind 0.0.0.0 --workers 4 hello:app -c conf.py
