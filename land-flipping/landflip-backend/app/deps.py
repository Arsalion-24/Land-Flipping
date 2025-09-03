from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
from .db import get_db
from . import models
from .security import decode_token

class CurrentUser:
    def __init__(self, user: Optional[models.User]):
        self.user = user

    @property
    def id(self) -> Optional[int]:
        return self.user.id if self.user else None

    @property
    def role(self) -> str:
        return self.user.role if self.user else "guest"

def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)) -> CurrentUser:
    if not authorization or not authorization.lower().startswith("bearer "):
        return CurrentUser(None)
    token = authorization.split(" ", 1)[1]
    payload = decode_token(token)
    if not payload:
        return CurrentUser(None)
    user = db.get(models.User, int(payload.get("sub")))
    return CurrentUser(user)

def require_role(role: str):
    def _inner(current: CurrentUser = Depends(get_current_user)):
        roles = [current.role]
        if current.role != role and role not in roles and current.role != "admin":
            raise HTTPException(status_code=403, detail="Forbidden")
        return current
    return _inner
