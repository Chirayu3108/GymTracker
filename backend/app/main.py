from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "App is live"}

@app.get("/health")
def health():
    return {"status": "OK"}
