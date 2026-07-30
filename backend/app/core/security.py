from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt

# ----------- For Settings Field Import ----------
from app.core.config import Settings
settings = Settings() # type: ignore[call-arg]
# ------------------------------------------------


# -------------------- Password Hashing & Verification -----------------------------
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def hash_password(password: str) -> str:
  return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
  return pwd_context.verify(plain_password, hashed_password)
# ----------------------------------------------------------------------------------


# ---------------------- Token Cretion, Encoding, & Decoding --------------------------
def create_access_token(subject: str) -> str:
  expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire)
  payload = {"sub": subject, "exp":expire}
  return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

def create_refresh_token(subject: str) -> str:
  expire = datetime.now(timezone.utc) + timedelta(days = settings.refresh_token_expire_days)
  payload = {"sub": subject, "exp" : expire}
  return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

def decode_token(token: str) -> dict:
  return jwt.decode(token, settings.secret_key, algorithms= [settings.algorithm])
# --------------------------------------------------------------------------------------

