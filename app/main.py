from fastapi import FastAPI
from time import time
from .middleware import logging_middleware

app = FastAPI()

app.add_middleware(logging_middleware)

START_TIME = time()
APP_VERSION = "0.1.0"


@app.get("/health")
def health():
    return {
        "status": "ok",
        "uptime_sec": round(time() - START_TIME, 2),
        "version": APP_VERSION,
    }
