from jose import jwt, JWTError
from passlib.context import CryptContext

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
def get_password_hash(password):
    try:
        return pwd_context.hash(password)
    except Exception as e:
        # Log or re-raise with helpful context
        raise Exception(f"Failed to hash password: {e}")

# Verify password
def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        # This usually means the hash is invalid or corrupted
        return False

# Create JWT token
def create_access_token(data: dict):
    try:
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    except JWTError as e:
        raise Exception(f"Token creation failed: {e}")
