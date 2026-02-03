from fastapi import FastAPI

app = FastAPI(title="Wildfire Detection API")

@app.get("/")
def read_root():
    return {"status": "ok", "service": "Wildfire Detection API"}
