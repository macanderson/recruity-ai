from fastapi import FastAPI, Request

from .routes.v1.hello import router as v1_router

app = FastAPI(title="Recruity AI API")

@app.middleware("http")
async def tenant_middleware(request: Request, call_next):
    tenant_id = request.headers.get("X-Tenant-ID")
    request.state.tenant_id = tenant_id
    response = await call_next(request)
    if tenant_id:
        response.headers["X-Tenant-ID"] = tenant_id
    return response


app.include_router(v1_router)
