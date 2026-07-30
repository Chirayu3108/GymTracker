from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ------------ Project File Imports ------------ 
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as user_router
# ----------------------------------------------



app = FastAPI()



# -------------- Routers ------------------------
app.include_router(auth_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
# -----------------------------------------------



# ------------- MiddleWare ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"], # fine for local dev, will lock this down before shipping
    allow_methods= ["*"],
    allow_headers= ["*"],
)
# -----------------------------------------



# ----------- Basic Endpoints -------------
@app.get("/")
def root():
    return {"message": "App is live"}

@app.get("/health")
def health():
    return {"status": "OK"}
# -----------------------------------------
