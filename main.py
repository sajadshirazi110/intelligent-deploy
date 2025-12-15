from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Intelligent Deploy Supervisor is running"}

@app.get("/health")
def health():
    return {"status": "ok"}
