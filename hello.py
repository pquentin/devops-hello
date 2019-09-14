import os

from random import randint
from flask import Flask
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics

os.environ.setdefault("prometheus_multiproc_dir", "/tmp")

app = Flask(__name__)
metrics = GunicornPrometheusMetrics(app)


@app.route("/")
def index():
    choice = ["/", "\\"]
    block = ""
    for i in range(80):
        line = "".join([ choice[randint(0, 1)] for i in range(350)])
        block+=line+"<br>"
    return block



def test_index():
    client = app.test_client()
    r = client.get("/")
    assert r.data[0] == b"/" or b"\\"
    assert r.data[-1] == b"/" or b"\\"
    assert r.status_code == 200
