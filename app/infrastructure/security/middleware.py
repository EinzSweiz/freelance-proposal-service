from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from starlette.responses import JSONResponse
from jose import jwt, JWTError
import os

# JWT конфигурация
SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-key")
ALGORITHM = "HS256"

# Публичные маршруты (без авторизации)
PUBLIC_PATHS = [
    "/docs",
    "/openapi.json"
]

def decode_token(token: str) -> dict:
    """Декодирует JWT токен."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Пропускаем публичные маршруты
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header missing or invalid"}
            )

        token = auth_header.split(" ")[1]

        try:
            payload = decode_token(token)
            request.state.user_id = payload.get("sub")
        except JWTError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or expired token"}
            )

        return await call_next(request)
