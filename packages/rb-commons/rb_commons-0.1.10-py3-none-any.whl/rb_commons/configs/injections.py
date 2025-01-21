from rb_commons.schemes.jwt import Claims
from fastapi import Request

async def get_claims(request: Request) -> Claims:
    return Claims.from_headers(dict(request.headers))