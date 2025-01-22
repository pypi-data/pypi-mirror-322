from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class UserIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")        
        request.state.user_id = user_id
        response = await call_next(request)
        return response