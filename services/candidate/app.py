from fastapi import FastAPI
from datetime import datetime
import random

app = FastAPI()

@app.get("/success")
def success():
    # igual al legacy
    return {"status": "ok", "value": 123, "source": "candidate"}

@app.get("/regression")
def regression():
    # regresión intencional (diferencia)
    return {"status": "ok", "value": 1000, "source": "candidate"}

@app.get("/noise")
def noise():
    # mismo "ruido" pero distinto rand -> mismatches por campos volátiles
    return {"status": "ok", "value": 42, "ts": datetime.utcnow().isoformat(), "rand": random.randint(1, 9999), "source": "candidate"}

@app.get("/health")
def health():
    return {"up": True, "service": "candidate"}
