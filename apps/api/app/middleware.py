from fastapi import Request

from .config import get_settings


async def tenant_middleware(request: Request, call_next):
    settings = get_settings()
    tenant_id = request.headers.get(settings.tenant_header)
    request.state.tenant_id = tenant_id
    response = await call_next(request)
    if tenant_id:
        response.headers[settings.tenant_header] = tenant_id
    return response
