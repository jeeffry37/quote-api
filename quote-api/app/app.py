from flask import Flask, jsonify, request
import random, json, os
from prometheus_client import Counter, Histogram, generate_latest

app = Flask(__name__)

# Métricas
REQUESTS = Counter("http_requests_total", "Total de requests", ["method", "endpoint", "status"])
LATENCY = Histogram("http_request_duration_seconds", "Latencia de requests", ["endpoint"])

# Cargar frases
QUOTES_PATH = os.getenv("QUOTES_PATH", "quotes.json")
with open(QUOTES_PATH, encoding="utf-8") as f:
    quotes = json.load(f)

def track(endpoint):
    def deco(fn):
        def wrapper(*args, **kwargs):
            with LATENCY.labels(endpoint=endpoint).time():
                resp = fn(*args, **kwargs)
            status = resp[1] if isinstance(resp, tuple) and len(resp) > 1 else 200
            REQUESTS.labels(method=request.method, endpoint=request.path, status=status).inc()
            return resp
        wrapper.__name__ = fn.__name__
        return wrapper
    return deco

@app.get("/")
def root():
    return {"message": "Welcome to Quote API! Try /quote or /quotes"}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/quote")
@track("/quote")
def get_quote():
    return jsonify({"quote": random.choice(quotes)})

@app.get("/quotes")
@track("/quotes")
def get_quotes():
    return jsonify(quotes)

@app.post("/quote")
@track("/quote")
def add_quote():
    data = request.get_json(silent=True) or {}
    q = (data.get("quote") or "").strip()
    if q:
        quotes.append(q)
        return {"message": "Quote added!"}, 201
    return {"error": "Missing 'quote' field"}, 400

@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain; charset=utf-8"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
