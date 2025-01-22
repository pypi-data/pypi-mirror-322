from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class TenantIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Pre-processing logic here
        print("Middleware: Before request")
        print(request.url)

        tenant_id = request.headers.get("X-Tenant-ID")
        if not tenant_id:
            raise HTTPException(status_code=400, detail="Tenant ID is required")
        
        request.state.tenant_id = tenant_id

        response = await call_next(request)

        # Post-processing logic here
        print("Middleware: After response")

        return response