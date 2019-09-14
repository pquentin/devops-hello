import os

from random import randint
from flask import Flask
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics

os.environ.setdefault("prometheus_multiproc_dir", "/tmp")

app = Flask(__name__)
metrics = GunicornPrometheusMetrics(app)

choice = ["/", "\\", " ", " ", " ", "_"]


@app.route("/")
def index():
    block = ""
    for i in range(80):
        line = "".join([ choice[randint(0, 5)] for i in range(350)])
        block+=line+"<br>"
    return "<pre>" + block + "</pre>"


def test_index():
    client = app.test_client()
    r = client.get("/")
    assert r.data
    assert r.status_code == 200
