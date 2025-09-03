from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from .db import SessionLocal
from . import models

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        try:
            db = SessionLocal()
            user_id = None
            auth = request.headers.get("authorization")
            if auth and auth.lower().startswith("bearer "):
                # lightweight parse; detailed user resolution done elsewhere
                user_id = None
            db.add(models.AuditLog(method=request.method, path=str(request.url.path), status_code=response.status_code, user_id=user_id))
            db.commit()
        except Exception:
            pass
        finally:
            try:
                db.close()
            except Exception:
                pass
        return response
