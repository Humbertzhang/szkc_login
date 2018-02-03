import json
import functools
import aiohttp
from aiohttp.web import Response

def require_szkc_login(f):
    @functools.wraps(f)
    async def decorator(request, *args, **kwargs):
        headers = dict(request.headers)
        BIGipServerpool = headers.get("Bigipserverpool")
        JSESSIONID = headers.get("Jsessionid")
        sid = headers.get("Sid")
        cookies = {
            'BIGipServerpool_xg_szxk':BIGipServerpool,
            'JSESSIONID':JSESSIONID
        }
        if BIGipServerpool_jwc_xk and JSESSIONID and sid:
            return await f(request, sid, cookies, *args, **kwargs)
        else:
            return Response(
                body = b'',
                content_type = 'application/json',
                status = 401
            )
        return decorator
