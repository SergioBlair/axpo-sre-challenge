import os
from storage import app
from waitress import serve
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST # we need prometheus_client library to import metrics
from flask import request, Response # and flask to manage HTTP requests and HTTP responses
import time

# Counter for counting requests number
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests (method, path, status)',
    ['method', 'path', 'status']
)

# Histogram for request latenct, in milliseconds
REQUEST_LATENCY = Histogram(
    'http_request_duration',
    'HTTP Request latency (milliseconds)',
    ['method', 'path', 'status']
)

# Middleware to track metrics
@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def track_metrics(response):
    request_latency = (time.time() - request.start_time) * 1_000  # Convert to milliseconds
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    REQUEST_LATENCY.labels(request.method, request.path, response.status_code).observe(request_latency)
    return response

# Endpoint for Prometheus in /metrics path as is usual in almost all exporters
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    port = os.getenv("PORT", default=5000)
    # Serve the app using Waitress, now including the Prometheus metrics endpoint
    serve(app, host="0.0.0.0", port=port)
