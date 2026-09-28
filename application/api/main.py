from fastapi import FastAPI

app = FastAPI(
    title="Production Reliability Engineering",
    version="0.1.0",
)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/ready")
def ready():
    return {"status": "ready"}


@app.get("/version")
def version():
    return {"version": app.version}
