from fastapi import FastAPI
from datetime import datetime
import random

app = FastAPI()

@app.get("/success")
def success():
    return {"status": "ok", "value": 123, "source": "legacy"}

@app.get("/regression")
def regression():
    # legacy devuelve un valor "correcto"
    return {"status": "ok", "value": 999, "source": "legacy"}

@app.get("/noise")
def noise():
    # ruido intencional (timestamps) para demostrar normalización/ruido
    return {"status": "ok", "value": 42, "ts": datetime.utcnow().isoformat(), "rand": random.randint(1, 9999), "source": "legacy"}

@app.get("/health")
def health():
    return {"up": True, "service": "legacy"}
