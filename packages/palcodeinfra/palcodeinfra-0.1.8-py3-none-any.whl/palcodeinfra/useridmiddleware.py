from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class UserIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Pre-processing logic here
        print("Middleware: Before request")
        print(request.url)

        user_id = request.headers.get("X-User-ID")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        
        request.state.tenant_id = user_id

        response = await call_next(request)

        # Post-processing logic here
        print("Middleware: After response")

        return response