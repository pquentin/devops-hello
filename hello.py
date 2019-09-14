import os

from flask import Flask
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics

os.environ.setdefault("prometheus_multiproc_dir", "/tmp")

app = Flask(__name__)
metrics = GunicornPrometheusMetrics(app)


@app.route("/")
def index():
    return "Hello Admin7, Admin6 is dead... A new World is coming! Will i have site unavailabe !"


def test_index():
    client = app.test_client()
    r = client.get("/")
    assert r.data == b"Hello Admin7, Admin6 is dead... A new World is coming! Will i have site unavailabe !"
    assert r.status_code == 200
