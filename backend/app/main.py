from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"], # fine for local dev, will lock this down before shipping
    allow_methods= ["*"],
    allow_headers= ["*"],
)

@app.get("/")
def root():
    return {"message": "App is live"}

@app.get("/health")
def health():
    return {"status": "OK"}
