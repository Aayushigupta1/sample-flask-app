from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, Gauge
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import os
import time

app = Flask(__name__)

# Feature Flag
NEW_FEATURE = os.getenv("NEW_FEATURE", "false").lower() == "true"

# Prometheus Metrics
REQUEST_COUNT = Counter(
    'flask_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'flask_request_duration_seconds',
    'Request processing time'
)

ACTIVE_REQUESTS = Gauge(
    'flask_active_requests',
    'Number of active HTTP requests'
)


@app.before_request
def before_request():
    request.start_time = time.time()
    ACTIVE_REQUESTS.inc()


@app.after_request
def after_request(response):
    if request.path != "/metrics":
        REQUEST_COUNT.labels(
            request.method,
            request.path,
            response.status_code
        ).inc()

        REQUEST_LATENCY.observe(
            time.time() - request.start_time
        )

    ACTIVE_REQUESTS.dec()
    return response


@app.route("/")
def home():
    if NEW_FEATURE:
        return """
        <h1>Welcome to New Dashboard</h1>
        <p>New Feature is ENABLED</p>
        """

    return """
    <h1>Welcome to Flask Application</h1>
    <p>New Feature is DISABLED</p>
    """


@app.route("/feature-status")
def feature_status():
    return jsonify({
        "new_feature": NEW_FEATURE,
        "status": "Enabled" if NEW_FEATURE else "Disabled"
    })


@app.route("/health")
def health():
    return jsonify({"status": "Application Running"})


# Prometheus Metrics Endpoint
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
