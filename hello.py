import os

from flask import Flask
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics

os.environ.setdefault("prometheus_multiproc_dir", "/tmp")

app = Flask(__name__)
metrics = GunicornPrometheusMetrics(app)


@app.route("/")
def index():
    return "Hello, Tib0 the world it's your!!"


def test_index():
    client = app.test_client()
    r = client.get("/")
    assert r.data == b"Hello, Tib0 the world it's your!!"
    assert r.status_code == 200
