from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class TokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth = request.headers.get("Authorization")
        if not auth:
            raise HTTPException(status_code=400, detail="Authorization header is required")        
        request.state.token = auth
        response = await call_next(request)
        return response