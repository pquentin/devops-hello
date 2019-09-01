import time

from flask import Flask
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics

app = Flask(__name__)
metrics = GunicornPrometheusMetrics(app)


@app.route('/')
def index():
    time.sleep(1)
    return 'Hello, World!'


def test_index():
    client = app.test_client()

    start = time.monotonic()
    r = client.get('/')
    end = time.monotonic()

    assert end - start >= 1.0
    assert r.data == b"Hello, World!"
    assert r.status_code == 200
